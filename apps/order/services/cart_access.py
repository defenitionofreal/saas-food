from apps.order.models import Cart


def cart_get_or_create(session_id: str, min_amount: int, institution, user) -> tuple:
    is_auth = user and user.is_authenticated
    # try to get current session's cart
    session_cart: Cart = Cart.objects.filter(institution=institution,
                                             session_id=session_id).first()

    if is_auth:
        # try to get user's cart from database
        db_cart: Cart = Cart.objects.filter(institution=institution,
                                            customer=user).first()
        if db_cart and session_cart:
            if db_cart.id == session_cart.id:
                return db_cart, False

            db_cart += session_cart
            session_cart.delete()
            db_cart.session_id = session_id
            db_cart.save()
            return db_cart, False
        elif db_cart and not session_cart:
            db_cart.session_id = session_id
            db_cart.save()
            return db_cart, False
        elif not db_cart and session_cart:
            session_cart.customer = user
            session_cart.save()
            return session_cart, False
        else:
            # create new cart for this user
            cart, cart_created = Cart.objects.get_or_create(
                institution=institution,
                customer=user,
                session_id=session_id,
                min_amount=min_amount)
            return cart, cart_created
    else:
        session_cart_belongs_to_user = session_cart and session_cart.customer is not None
        if session_cart_belongs_to_user:
            """
            invalidate session_id for existing cart
            to prevent anonymous access to someone cart
            """
            session_cart.session_id = None
            session_cart.save()

        # create new anonymous cart
        cart, cart_created = Cart.objects.get_or_create(
            institution=institution,
            session_id=session_id,
            min_amount=min_amount)
        return cart, cart_created
