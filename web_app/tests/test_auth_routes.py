from unittest.mock import patch

def test_login_get_renders_users(client, mock_user_repo):
    # Gọi GET
    res = client.get('/auth/login')
    assert res.status_code == 200

    # Lấy tất cả user từ repo để kiểm tra tên có render ra không
    users = mock_user_repo.get_all()
    content = res.get_data(as_text=True)
    for user in users:
        assert user.Name in content


def test_login_post_sets_session(client, mock_user_repo):
    user = mock_user_repo.get_all()[0]

    with patch("web_app.services.auth_service.url_for", return_value="/fake-home"):
        res = client.post('/auth/login', data={'user_id': str(user.Id)}, follow_redirects=False)

    with client.session_transaction() as sess:
        assert sess['user_id'] == user.Id

    assert res.status_code == 302


def test_logout_clears_session(client, mock_user_repo):
    # Đặt session giả
    with client.session_transaction() as sess:
        sess['user_id'] = 123

    # Gọi logout
    res = client.get('/auth/logout', follow_redirects=False)

    # Kiểm tra session đã bị xóa
    with client.session_transaction() as sess:
        assert 'user_id' not in sess

    assert res.status_code == 302
