from http import HTTPStatus

import pytest

from tests.test_company.factories import InstitutionFactory
from tests.test_product.factories import CategoryFactory, ProductFactory, ModifierFactory, ModifierPriceFactory, \
    AdditiveFactory, CategoryAdditiveFactory


@pytest.fixture()
def institution(user):
    return InstitutionFactory.create(user=user)


@pytest.fixture()
def categories(institution):
    category_kwargs = {"institution": institution, "is_active": True}
    return (
        CategoryFactory.create(title="Pizza", slug="pizza", **category_kwargs),
        CategoryFactory.create(title="Drink", slug="drinks", **category_kwargs),
    )


@pytest.fixture()
def products(institution, categories):
    product_kwargs = {"institution": institution, "is_active": True}
    return (
        ProductFactory.create(
            category=categories[0],
            title="Margarita",
            description="Margarita",
            **product_kwargs,
        ),
        ProductFactory.create(
            category=categories[1],
            title="Coca cola",
            description="Coca cola",
            **product_kwargs,
        ),
    )


def test_add_product(user, institution, products, api_client):
    """Test add product to cart."""
    product_data = {
        "product": products[0].id,
        "modifiers": [],
        "additives": [],
        "quantity": 2,
    }

    api_client.login_user(user)
    response = api_client.post(
        "/api/order/{0}/customer/cart/product/".format(institution.domain),
        data=product_data,
        format="json",
    )
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert user.cart_customer.cart_products.count() == 1

    cart_product = user.cart_customer.cart_products.first()

    assert cart_product.product == products[0]
    assert cart_product.quantity == 2
    assert not cart_product.modifiers.exists()
    assert not cart_product.additives.exists()


def test_add_product_modifier(user, institution, products, api_client):
    """Test add product with modifier to cart."""
    modifier = ModifierFactory.create(institution=institution)
    ModifierPriceFactory.create(
        institution=institution,
        product=products[0],
        modifier=modifier,
    )
    products[0].modifiers.set([modifier])

    product_data = {
        "product": products[0].id,
        "modifiers": [modifier.id],
        "additives": [],
        "quantity": 3,
    }

    api_client.login_user(user)
    response = api_client.post(
        "/api/order/{0}/customer/cart/product/".format(institution.domain),
        data=product_data,
        format="json",
    )
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert user.cart_customer.cart_products.count() == 1

    cart_product = user.cart_customer.cart_products.first()

    assert cart_product.product == products[0]
    assert cart_product.quantity == 3
    assert cart_product.modifiers.count() == 1
    assert cart_product.modifiers.first() == modifier
    assert not cart_product.additives.exists()


def test_add_product_modifier_wrong(user, institution, products, api_client):
    """Test modifier not in product.modifiers."""
    modifier = ModifierFactory.create(institution=institution)
    ModifierPriceFactory.create(
        institution=institution,
        product=products[0],
        modifier=modifier,
    )

    product_data = {
        "product": products[0].id,
        "modifiers": [modifier.id],
        "additives": [],
        "quantity": 3,
    }

    api_client.login_user(user)
    response = api_client.post(
        "/api/order/{0}/customer/cart/product/".format(institution.domain),
        data=product_data,
        format="json",
    )
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert not user.cart_customer.cart_products.exists()


def test_add_product_additive(user, institution, products, api_client):
    """Test add product with additive to cart."""
    category = CategoryAdditiveFactory.create(institution=institution)
    additive = AdditiveFactory.create(institution=institution, category=category)
    products[0].additives.set([category])

    product_data = {
        "product": products[0].id,
        "modifiers": [],
        "additives": [additive.id],
        "quantity": 4,
    }

    api_client.login_user(user)
    response = api_client.post(
        "/api/order/{0}/customer/cart/product/".format(institution.domain),
        data=product_data,
        format="json",
    )
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert user.cart_customer.cart_products.count() == 1

    cart_product = user.cart_customer.cart_products.first()

    assert cart_product.product == products[0]
    assert cart_product.quantity == 4
    assert not cart_product.modifiers.exists()
    assert cart_product.additives.count() == 1
    assert cart_product.additives.first() == additive


def test_add_product_additive_wrong(user, institution, products, api_client):
    """Test add product with additive to cart."""
    category = CategoryAdditiveFactory.create(institution=institution)
    additive = AdditiveFactory.create(institution=institution, category=category, is_active=False)
    products[0].additives.set([category])

    product_data = {
        "product": products[0].id,
        "modifiers": [],
        "additives": [additive.id],
        "quantity": 4,
    }

    api_client.login_user(user)
    response = api_client.post(
        "/api/order/{0}/customer/cart/product/".format(institution.domain),
        data=product_data,
        format="json",
    )
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert not user.cart_customer.cart_products.exists()


def test_add_product_modifier_and_additive(user, institution, products, api_client):
    """Test add product with modifier and additive to cart."""
    modifier = ModifierFactory.create(institution=institution)
    ModifierPriceFactory.create(
        institution=institution,
        product=products[0],
        modifier=modifier,
    )
    category = CategoryAdditiveFactory.create(institution=institution)
    additive = AdditiveFactory.create(institution=institution, category=category)

    products[0].modifiers.set([modifier])
    products[0].additives.set([category])

    product_data = {
        "product": products[0].id,
        "modifiers": [modifier.id],
        "additives": [additive.id],
        "quantity": 4,
    }

    api_client.login_user(user)
    response = api_client.post(
        "/api/order/{0}/customer/cart/product/".format(institution.domain),
        data=product_data,
        format="json",
    )
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert user.cart_customer.cart_products.count() == 1

    cart_product = user.cart_customer.cart_products.first()

    assert cart_product.product == products[0]
    assert cart_product.quantity == 4
    assert cart_product.modifiers.count() == 1
    assert cart_product.modifiers.first() == modifier
    assert cart_product.additives.count() == 1
    assert cart_product.additives.first() == additive


def test_merge_products(user, institution, products, api_client):
    """Test merge equal products."""
    modifier = ModifierFactory.create(institution=institution)
    ModifierPriceFactory.create(
        institution=institution,
        product=products[0],
        modifier=modifier,
    )
    category = CategoryAdditiveFactory.create(institution=institution)
    additive = AdditiveFactory.create(institution=institution, category=category)

    products[0].modifiers.set([modifier])
    products[0].additives.set([category])

    product_data = {
        "product": products[0].id,
        "modifiers": [modifier.id],
        "additives": [additive.id],
        "quantity": 1,
    }

    api_client.login_user(user)
    response = api_client.post(
        "/api/order/{0}/customer/cart/product/".format(institution.domain),
        data=product_data,
        format="json",
    )
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert user.cart_customer.cart_products.count() == 1

    cart_product = user.cart_customer.cart_products.first()

    assert cart_product.product == products[0]
    assert cart_product.quantity == 1
    assert cart_product.modifiers.count() == 1
    assert cart_product.modifiers.first() == modifier
    assert cart_product.additives.count() == 1
    assert cart_product.additives.first() == additive

    # add equal product
    product_data["quantity"] = 2
    response = api_client.post(
        "/api/order/{0}/customer/cart/product/".format(institution.domain),
        data=product_data,
        format="json",
    )

    assert response.status_code == HTTPStatus.OK
    assert user.cart_customer.cart_products.count() == 1

    cart_product = user.cart_customer.cart_products.first()

    assert cart_product.product == products[0]
    assert cart_product.quantity == 3
    assert cart_product.modifiers.count() == 1
    assert cart_product.modifiers.first() == modifier
    assert cart_product.additives.count() == 1
    assert cart_product.additives.first() == additive
