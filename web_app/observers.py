class Event:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, fn):
        self.subscribers.append(fn)

    def notify(self, *args, **kwargs):
        for fn in self.subscribers:
            fn(*args, **kwargs)

# Khai báo các sự kiện toàn cục (event bus)
on_post_save = Event()
on_user_follow = Event()
on_trigger_create = Event()


def email_on_post_save(post, user):
    print(f"Send email: User {user.Name} saved Post '{post.Title}'")

def log_user_follow(user, post):
    print(f"Log: User {user.Name} followed Post '{post.Title}'")

def email_on_trigger_create(user, post):
    print(f"Send email: Notification triggered for user {user.Name} on post '{post.Title}'")

# Đăng ký hàm vào sự kiện
on_post_save.subscribe(email_on_post_save)
on_user_follow.subscribe(log_user_follow)
on_trigger_create.subscribe(email_on_trigger_create)
