from uuid import uuid4, UUID
import mock
from django.test import TestCase
import pytest

from enterprise_access.apps.subsidy.models import *
from enterprise_access.apps.ledger.models import Ledger, Transaction, Reversal, UnitChoices
from enterprise_access.apps.subsidy import api as subsidy_api
from enterprise_access.apps.ledger import api as ledger_api

@pytest.fixture
def group_a():
    return {
        'uuid': uuid4(),
    }


@pytest.fixture
def catalog_a():
    return {
        'uuid': uuid4(),
    }


@pytest.fixture
def ledger_fixture():
    ledger_idp_key = uuid4()
    ledger = ledger_api.create_ledger(
        unit=UnitChoices.SEATS,
        idempotency_key=ledger_idp_key,
    )
    ledger_api.create_transaction(
        ledger,
        quantity=100,
        idempotency_key=f'ledger-{ledger_idp_key}-init-100',
    )
    return ledger


@pytest.fixture
def subscription_subsidy():
    return subsidy_api.create_subscription_subsidy(
        customer_uuid=uuid4(),
        subscription_plan_uuid=uuid4(),
        unit=UnitChoices.SEATS,
        starting_balance=100,
    )


@pytest.fixture
def policy_fixture(group_a, subscription_subsidy, catalog_a):
    policy = SubscriptionAccessPolicy.objects.create(
        group_uuid=group_a['uuid'],
        subsidy=subscription_subsidy,
        catalog_uuid=catalog_a['uuid'],
        total_value=50,
    )
    # make it so any learner is always in the group for this policy
    policy.group_client.get_groups_for_learner.return_value = [
        {'uuid': policy.group_uuid},
    ]
    return policy


@pytest.mark.django_db
def test_create_subsidy_happy_path(subscription_subsidy):
    assert subscription_subsidy.unit == UnitChoices.SEATS


@pytest.mark.django_db
def test_subscription_subsidy_policy_happy_paths(policy_fixture):
    assert policy_fixture.total_value == 50
    some_learner_id = 'abcde12345'
    assert policy_fixture.subsidy.get_license_for_learner(some_learner_id)['uuid'] is not None

    # Test the flow for checking if a learner is entitled to a subscription plan's license
    # make the learner not have a license yet.
    policy_fixture.subsidy.subscription_client.get_license_for_learner.return_value = None
    # makes is_redeemable() return True
    policy_fixture.subsidy.subscription_client.get_plan_metadata.return_value = {'licenses': {'pending': 50}}

    assert policy_fixture.is_learner_entitled_to_subsidy(some_learner_id)

    # Test the flow for giving the license as an entitlement
    # subsidy.create_redemption() is mocked to return a "license uuid" in its implementation
    granted_license_entitlement = policy_fixture.give_entitlement_to_subsidy(some_learner_id)
    assert granted_license_entitlement == {
        'status': 'activated',
        'uuid': mock.ANY,
    }
    assert type(granted_license_entitlement['uuid']) == UUID

    # Test the flow for checking if learner may redeem their entitlement for content
    # in the subscription subsidy
    policy_fixture.catalog_client.catalog_contains_content.return_value = True
    policy_fixture.subsidy.subscription_client.get_license_for_learner.return_value = {
        'uuid': uuid4(),
    }
    some_content_key = 'doesnt matter'
    assert policy_fixture.can_learner_redeem_for_content(some_learner_id, some_content_key)

    # Test the flow where a learner redeems the license to which they are entitled
    # in the context of a specific content key
    assert policy_fixture.redeem_for_content(some_learner_id, some_content_key)


@pytest.mark.django_db
def test_subsidy_has_balance(subscription_subsidy):
    assert subscription_subsidy.unit == UnitChoices.SEATS
    subscription_subsidy.subscription_client.get_plan_metadata.return_value = {
        'licenses': {'pending': 50, 'total': 100}
    }
    subsidy_api.sync_subscription(subscription_subsidy, request_user='bob')
    # TODO: explain the subtlety that results in a "fresh" subscription balance being zero
    assert subscription_subsidy.current_balance() == 0
