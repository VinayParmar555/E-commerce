import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from datetime import datetime, timedelta, timezone

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def make_mock_user(id=1, name="Test", email="test@example.com", is_admin=False, is_verified=True):
    user = MagicMock()
    user.id = id
    user.name = name
    user.email = email
    user.is_admin = is_admin
    user.is_verified = is_verified
    user.hashed_password = "$2b$12$hashedpassword"
    return user

def make_mock_product(id=1, name="Phone", price=999.0, description="A phone", quantity=10, category_id=1):
    product = MagicMock()
    product.id = id
    product.name = name
    product.price = price
    product.description = description
    product.quantity = quantity
    product.category_id = category_id
    cat = MagicMock()
    cat.name = "Electronics"
    product.category = cat
    return product

def make_mock_cart_item(id=1, user_id=1, product_id=1, quantity=2, price=500.0, total_price=1000.0):
    item = MagicMock()
    item.id = id
    item.user_id = user_id
    item.product_id = product_id
    item.quantity = quantity
    item.price = price
    item.total_price = total_price
    return item


# ─────────────────────────────────────────────────────────────
# Auth Service Tests
# ─────────────────────────────────────────────────────────────

class TestAuthService:

    def test_create_user_success(self):
        from app.services.auth_service import create_user
        from app.schema.user import UserCreate

        db = MagicMock()
        db.query().filter().first.return_value = None
        mock_user = MagicMock()
        mock_user.id = 1
        db.add.return_value = None
        db.refresh.side_effect = lambda x: setattr(x, 'id', 1)
        user_data = UserCreate(name="John", email="john@example.com", password="pass123")

        with patch("app.services.auth_service.hash_password", return_value="hashed"):
            result = create_user(db, user_data)

        db.add.assert_called_once()
        db.commit.assert_called_once()
        assert result is not False

    def test_create_user_duplicate_email(self):
        from app.services.auth_service import create_user
        from app.schema.user import UserCreate

        db = MagicMock()
        db.query().filter().first.return_value = make_mock_user()
        user_data = UserCreate(name="John", email="test@example.com", password="pass123")

        result = create_user(db, user_data)
        assert result is False

    def test_authenticate_user_success(self):
        from app.services.auth_service import authenticate_user

        mock_user = make_mock_user()
        db = MagicMock()
        db.query().filter().first.return_value = mock_user

        with patch("app.services.auth_service.verify_password", return_value=True):
            result = authenticate_user(db, "test@example.com", "password")

        assert result == mock_user

    def test_authenticate_user_wrong_password(self):
        from app.services.auth_service import authenticate_user

        db = MagicMock()
        db.query().filter().first.return_value = make_mock_user()

        with patch("app.services.auth_service.verify_password", return_value=False):
            result = authenticate_user(db, "test@example.com", "wrong")

        assert result is None

    def test_authenticate_user_not_found(self):
        from app.services.auth_service import authenticate_user

        db = MagicMock()
        db.query().filter().first.return_value = None

        result = authenticate_user(db, "nope@example.com", "password")
        assert result is None

    def test_create_tokens(self):
        from app.services.auth_service import create_tokens

        db = MagicMock()
        db.query().filter().update.return_value = 0
        mock_user = make_mock_user()

        with patch("app.services.auth_service.create_access_token", return_value="access_tok"):
            result = create_tokens(db, mock_user)

        assert "access_token" in result
        assert "refresh_token" in result
        assert result["access_token"] == "access_tok"
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_verify_refresh_token_valid(self):
        from app.services.auth_service import verify_refresh_token

        db = MagicMock()
        mock_token = MagicMock()
        mock_token.revoked = False
        mock_token.expires_at = datetime.now(timezone.utc) + timedelta(days=1)
        mock_token.user_id = 1
        db.query().filter().first.return_value = mock_token

        mock_user = make_mock_user()
        db.query().filter().first.side_effect = [mock_token, mock_user]

        result = verify_refresh_token(db, "valid-token")
        # Result should be the user (from second query)
        assert result is not None

    def test_verify_refresh_token_expired(self):
        from app.services.auth_service import verify_refresh_token

        db = MagicMock()
        mock_token = MagicMock()
        mock_token.revoked = False
        mock_token.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        db.query().filter().first.return_value = mock_token

        result = verify_refresh_token(db, "expired-token")
        assert result is None

    def test_verify_email_token_success(self):
        from app.services.auth_service import verify_email_token

        db = MagicMock()
        mock_user = make_mock_user()
        mock_user.is_verified = False
        db.query().filter().first.return_value = mock_user

        with patch("app.services.auth_service.verify_token_and_get_user_id", return_value=1):
            result = verify_email_token(db, "valid-email-token")

        assert result is True
        assert mock_user.is_verified is True
        db.commit.assert_called_once()

    def test_verify_email_token_invalid(self):
        from app.services.auth_service import verify_email_token

        db = MagicMock()
        with patch("app.services.auth_service.verify_token_and_get_user_id", return_value=None):
            result = verify_email_token(db, "invalid-token")
        assert result is None

    def test_email_verification_process(self):
        from app.services.auth_service import email_verification_process

        bg_tasks = MagicMock()
        mock_user = make_mock_user()

        with patch("app.services.auth_service.create_email_verification_token", return_value="tok123"):
            result = email_verification_process(bg_tasks, mock_user)

        bg_tasks.add_task.assert_called_once()
        assert "msg" in result

    def test_cleanup_expired_tokens(self):
        from app.services.auth_service import cleanup_expired_tokens

        db = MagicMock()
        db.query().filter().delete.return_value = 5

        result = cleanup_expired_tokens(db)
        assert result == 5
        db.commit.assert_called_once()


# ─────────────────────────────────────────────────────────────
# Product Service Tests
# ─────────────────────────────────────────────────────────────

class TestProductService:

    def test_list_of_products(self):
        from app.services.product_service import List_of_products

        db = MagicMock()
        mock_products = [make_mock_product(), make_mock_product(id=2)]
        db.query().options().all.return_value = mock_products

        result = List_of_products(db)
        assert len(result) == 2

    def test_list_of_products_empty(self):
        from app.services.product_service import List_of_products

        db = MagicMock()
        db.query().options().all.return_value = []

        result = List_of_products(db)
        assert result is False

    def test_search_product_found(self):
        from app.services.product_service import search_product

        db = MagicMock()
        mock_prod = make_mock_product()
        db.query().options().filter().first.return_value = mock_prod

        result = search_product(db, 1)
        assert result["name"] == "Phone"

    def test_search_product_not_found(self):
        from app.services.product_service import search_product

        db = MagicMock()
        db.query().options().filter().first.return_value = None

        result = search_product(db, 999)
        assert result is False

    def test_add_product(self):
        from app.services.product_service import add_product
        from app.schema.products import ProductCreate

        db = MagicMock()
        product_data = ProductCreate(name="Laptop", price=1500.0, description="A laptop", quantity=5, category_id=1)

        result = add_product(db, product_data)
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_update_product_found(self):
        from app.services.product_service import update_product
        from app.schema.products import ProductCreate

        db = MagicMock()
        mock_prod = make_mock_product()
        db.get.return_value = mock_prod
        update_data = ProductCreate(name="Updated", price=100.0, description="Updated", quantity=5, category_id=1)

        result = update_product(db, 1, update_data)
        db.commit.assert_called_once()
        assert result is not False

    def test_update_product_not_found(self):
        from app.services.product_service import update_product
        from app.schema.products import ProductCreate

        db = MagicMock()
        db.get.return_value = None
        update_data = ProductCreate(name="Updated", price=100.0, description="Updated", quantity=5, category_id=1)

        result = update_product(db, 999, update_data)
        assert result is False

    def test_delete_product_found(self):
        from app.services.product_service import delete_product

        db = MagicMock()
        mock_prod = make_mock_product()
        db.get.return_value = mock_prod

        result = delete_product(db, 1)
        db.delete.assert_called_once_with(mock_prod)
        db.commit.assert_called_once()

    def test_delete_product_not_found(self):
        from app.services.product_service import delete_product

        db = MagicMock()
        db.get.return_value = None

        result = delete_product(db, 999)
        assert result is False

    def test_pagination_process(self):
        from app.services.product_service import pagination_process

        db = MagicMock()
        mock_products = [make_mock_product()]
        db.query().offset().limit().all.return_value = mock_products

        result = pagination_process(db, page=1, limit=10)
        assert len(result) == 1


# ─────────────────────────────────────────────────────────────
# Cart Service Tests
# ─────────────────────────────────────────────────────────────

class TestCartService:

    def test_add_to_cart_new_item(self):
        from app.services.cart_service import add_to_cart
        from app.schema.cart import CartItem

        db = MagicMock()
        mock_user = make_mock_user()
        db.get.return_value = mock_user

        mock_prod = make_mock_product(quantity=10)
        db.query().filter().first.side_effect = [mock_prod, None]  # product found, no existing cart

        cart_data = CartItem(quantity=2, product_id=1)
        result = add_to_cart(db, cart_data, 1)

        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_add_to_cart_insufficient_stock(self):
        from app.services.cart_service import add_to_cart
        from app.schema.cart import CartItem

        db = MagicMock()
        db.get.return_value = make_mock_user()
        mock_prod = make_mock_product(quantity=0)
        db.query().filter().first.return_value = mock_prod

        cart_data = CartItem(quantity=5, product_id=1)
        result = add_to_cart(db, cart_data, 1)
        assert result is None

    def test_add_to_cart_user_not_found(self):
        from app.services.cart_service import add_to_cart
        from app.schema.cart import CartItem

        db = MagicMock()
        db.get.return_value = None

        cart_data = CartItem(quantity=1, product_id=1)
        result = add_to_cart(db, cart_data, 999)
        assert result is False

    def test_see_cart_with_items(self):
        from app.services.cart_service import see_cart

        db = MagicMock()
        mock_items = [make_mock_cart_item(), make_mock_cart_item(id=2)]
        db.query().filter().all.return_value = mock_items

        result = see_cart(db, 1)
        assert "items" in result
        assert "total_price" in result

    def test_see_cart_empty(self):
        from app.services.cart_service import see_cart

        db = MagicMock()
        db.query().filter().all.return_value = []

        result = see_cart(db, 1)
        assert result is None

    def test_remove_cart_success(self):
        from app.services.cart_service import remove_cart

        db = MagicMock()
        mock_cart = make_mock_cart_item()
        db.query().filter().first.return_value = mock_cart

        result = remove_cart(db, 1, 1)
        assert result is True
        db.delete.assert_called_once_with(mock_cart)

    def test_remove_cart_not_found(self):
        from app.services.cart_service import remove_cart

        db = MagicMock()
        db.query().filter().first.return_value = None

        result = remove_cart(db, 1, 999)
        assert result is None


# ─────────────────────────────────────────────────────────────
# User Service Tests
# ─────────────────────────────────────────────────────────────

class TestUserService:

    def test_change_password_success(self):
        from app.services.user_service import change_password_process

        db = MagicMock()
        mock_user = make_mock_user()

        with patch("app.services.user_service.verify_password", return_value=True), \
             patch("app.services.user_service.hash_password", return_value="new_hashed"):
            result = change_password_process(db, mock_user, "oldpass", "newpass")

        assert result is True
        db.commit.assert_called_once()

    def test_change_password_wrong_old(self):
        from app.services.user_service import change_password_process

        db = MagicMock()
        mock_user = make_mock_user()

        with patch("app.services.user_service.verify_password", return_value=False):
            result = change_password_process(db, mock_user, "wrong", "newpass")

        assert result is None

    def test_promote_admin_success(self):
        from app.services.user_service import promote_admin

        db = MagicMock()
        mock_user = make_mock_user(is_admin=False)
        db.get.return_value = mock_user

        result = promote_admin(db, 1)
        assert result is True
        assert mock_user.is_admin is True

    def test_promote_admin_already_admin(self):
        from app.services.user_service import promote_admin

        db = MagicMock()
        mock_user = make_mock_user(is_admin=True)
        db.get.return_value = mock_user

        result = promote_admin(db, 1)
        assert result is False

    def test_promote_admin_user_not_found(self):
        from app.services.user_service import promote_admin

        db = MagicMock()
        db.get.return_value = None

        result = promote_admin(db, 999)
        assert result is None

    def test_revoke_token_success(self):
        from app.services.user_service import revoke_token

        db = MagicMock()
        mock_token = MagicMock()
        mock_token.revoked = False
        db.query().filter().first.return_value = mock_token

        result = revoke_token(db, "token123")
        assert result is True
        assert mock_token.revoked is True

    def test_revoke_token_not_found(self):
        from app.services.user_service import revoke_token

        db = MagicMock()
        db.query().filter().first.return_value = None

        result = revoke_token(db, "nonexistent")
        assert result is False

    def test_delete_user_success(self):
        from app.services.user_service import delete_user

        db = MagicMock()
        mock_user = make_mock_user()
        db.get.return_value = mock_user

        result = delete_user(db, 1)
        assert result is True
        db.delete.assert_called_once_with(mock_user)

    def test_delete_user_not_found(self):
        from app.services.user_service import delete_user

        db = MagicMock()
        db.get.return_value = None

        result = delete_user(db, 999)
        assert result is None

    def test_reset_password_process_success(self):
        from app.services.user_service import reset_password_process

        db = MagicMock()
        mock_user = make_mock_user()
        db.query().filter().first.return_value = mock_user
        bg_tasks = MagicMock()

        with patch("app.services.user_service.create_password_reset_token", return_value="reset_tok"):
            result = reset_password_process(db, "test@example.com", bg_tasks)

        assert result is True
        bg_tasks.add_task.assert_called_once()

    def test_reset_password_process_email_not_found(self):
        from app.services.user_service import reset_password_process

        db = MagicMock()
        db.query().filter().first.return_value = None
        bg_tasks = MagicMock()

        result = reset_password_process(db, "nope@example.com", bg_tasks)
        assert result is None


# ─────────────────────────────────────────────────────────────
# Category Service Tests
# ─────────────────────────────────────────────────────────────

class TestCategoryService:

    def test_add_category(self):
        from app.services.category_service import add_categories
        from app.schema.category import CategoryBase

        db = MagicMock()
        cat_data = CategoryBase(name="Electronics")

        result = add_categories(db, cat_data)
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_get_categories(self):
        from app.services.category_service import get_categories

        db = MagicMock()
        db.query().all.return_value = [MagicMock(id=1, name="Electronics")]

        result = get_categories(db)
        assert len(result) == 1

    def test_get_categories_empty(self):
        from app.services.category_service import get_categories

        db = MagicMock()
        db.query().all.return_value = []

        result = get_categories(db)
        assert result is False

    def test_update_category_success(self):
        from app.services.category_service import update_category
        from app.schema.category import CategoryBase

        db = MagicMock()
        mock_cat = MagicMock()
        db.get.return_value = mock_cat

        result = update_category(db, 1, CategoryBase(name="Updated"))
        assert result is not False
        db.commit.assert_called_once()

    def test_update_category_not_found(self):
        from app.services.category_service import update_category
        from app.schema.category import CategoryBase

        db = MagicMock()
        db.get.return_value = None

        result = update_category(db, 999, CategoryBase(name="Nope"))
        assert result is False

    def test_delete_category_success(self):
        from app.services.category_service import delete_category

        db = MagicMock()
        mock_cat = MagicMock()
        db.get.return_value = mock_cat

        result = delete_category(db, 1)
        assert result is True
        db.delete.assert_called_once()

    def test_delete_category_not_found(self):
        from app.services.category_service import delete_category

        db = MagicMock()
        db.get.return_value = None

        result = delete_category(db, 999)
        assert result is False


# ─────────────────────────────────────────────────────────────
# Shipping Service Tests
# ─────────────────────────────────────────────────────────────

class TestShippingService:

    def test_create_shipping_address(self):
        from app.services.shipping_service import create_shipping_address
        from app.schema.shipping import ShippingBase

        db = MagicMock()
        data = ShippingBase(
            address_line1="123 Main St", city="Mumbai",
            postal_code=400001, state="MH", country="India"
        )

        result = create_shipping_address(db, 1, data)
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_fetch_address_found(self):
        from app.services.shipping_service import fetch_address

        db = MagicMock()
        db.query().filter().all.return_value = [MagicMock()]

        result = fetch_address(db, 1)
        assert result is not None

    def test_fetch_address_empty(self):
        from app.services.shipping_service import fetch_address

        db = MagicMock()
        db.query().filter().all.return_value = []

        result = fetch_address(db, 1)
        assert result is None

    def test_delete_address_success(self):
        from app.services.shipping_service import delete_address

        db = MagicMock()
        mock_addr = MagicMock()
        db.query().filter().first.return_value = mock_addr

        result = delete_address(db, 1, 1)
        assert result is True
        db.delete.assert_called_once()

    def test_delete_address_not_found(self):
        from app.services.shipping_service import delete_address

        db = MagicMock()
        db.query().filter().first.return_value = None

        result = delete_address(db, 1, 999)
        assert result is None


# ─────────────────────────────────────────────────────────────
# Payment Service Tests (with mocked Razorpay)
# ─────────────────────────────────────────────────────────────

class TestPaymentService:

    def test_create_mock_payment_success(self):
        from app.services.payment_service import create_payment
        from app.schema.payment import PaymentCreate, PaymentGateway

        db = MagicMock()
        def _refresh(obj):
            obj.id = 1
            obj.created_at = datetime.now(timezone.utc)
            obj.updated_at = datetime.now(timezone.utc)
        db.refresh.side_effect = _refresh
        order = MagicMock()
        order.id = 1
        order.user_id = 1
        order.total_price = 1000  
        data = PaymentCreate(amount=1000, shipping_address_id=1, gateway=PaymentGateway.mock, simulate_succ=True)

        result = create_payment(db, 1, order, data)
        assert result is not None
        assert result.payment is not None
        db.add.assert_called()
        db.commit.assert_called()

    def test_create_mock_payment_failure(self):
        from app.services.payment_service import create_payment
        from app.schema.payment import PaymentCreate, PaymentGateway

        db = MagicMock()
        def _refresh(obj):
            obj.id = 1
            obj.created_at = datetime.now(timezone.utc)
            obj.updated_at = datetime.now(timezone.utc)
        db.refresh.side_effect = _refresh
        order = MagicMock()
        order.id = 1
        data = PaymentCreate(amount=1000, shipping_address_id=1, gateway=PaymentGateway.mock, simulate_succ=False)

        result = create_payment(db, 1, order, data)
        assert result is not None
        # Payment should be failed
        assert result.payment is not None

    @patch("app.services.payment_service._razorpay_client")
    def test_create_razorpay_payment(self, mock_rz_client):
        from app.services.payment_service import create_payment
        from app.schema.payment import PaymentCreate, PaymentGateway

        mock_rz_client.order.create.return_value = {"id": "order_123"}

        db = MagicMock()
        def _refresh(obj):
            obj.id = 1
            obj.created_at = datetime.now(timezone.utc)
            obj.updated_at = datetime.now(timezone.utc)
        db.refresh.side_effect = _refresh
        order = MagicMock()
        order.id = 1
        data = PaymentCreate(amount=1000, shipping_address_id=1, gateway=PaymentGateway.razorpay)

        result = create_payment(db, 1, order, data)
        assert result is not None
        assert result.rz_data is not None
        assert result.rz_data["pg_order_id"] == "order_123"

    @patch("app.services.payment_service._razorpay_client")
    def test_create_razorpay_payment_failure(self, mock_rz_client):
        from app.services.payment_service import create_payment
        from app.schema.payment import PaymentCreate, PaymentGateway
        from app.exception.checkout import RazorpayPaymentFailed

        mock_rz_client.order.create.side_effect = Exception("API Error")

        db = MagicMock()
        order = MagicMock()
        order.id = 1
        data = PaymentCreate(amount=1000, shipping_address_id=1, gateway=PaymentGateway.razorpay)

        with pytest.raises(RazorpayPaymentFailed):
            create_payment(db, 1, order, data)

    def test_fetch_payment_status_found(self):
        from app.services.payment_service import fetch_payment_status

        db = MagicMock()
        mock_payment = MagicMock()
        db.query().filter().first.return_value = mock_payment

        result = fetch_payment_status(db, 1, 1)
        assert result == mock_payment

    def test_fetch_payment_status_not_found(self):
        from app.services.payment_service import fetch_payment_status

        db = MagicMock()
        db.query().filter().first.return_value = None

        result = fetch_payment_status(db, 1, 999)
        assert result is None

    def test_fetch_all_payments(self):
        from app.services.payment_service import fetch_all_payments

        db = MagicMock()
        db.query().filter().all.return_value = [MagicMock(), MagicMock()]

        result = fetch_all_payments(db, 1)
        assert len(result) == 2

    def test_fetch_all_payments_empty(self):
        from app.services.payment_service import fetch_all_payments

        db = MagicMock()
        db.query().filter().all.return_value = []

        result = fetch_all_payments(db, 1)
        assert result is None
