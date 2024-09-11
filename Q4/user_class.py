class USER:
    def __init__(self, user_id, name, email, age, signup_date, bank_balance, debt):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.signup_date = signup_date
        self.bank_balance = bank_balance
        self.debt = debt

    def email_current_balance(self):
        print(f"Email to {self.email}:")
        print(f"Dear {self.name},")
        print(f"Your current bank balance is: ${self.bank_balance:.2f}")
        print(f"Your outstanding debt is: ${self.debt:.2f}")
        print("Thank you for banking with us!\n")

    @staticmethod
    def sort_users_by_name(users):
        if len(users) <= 1:
            return users
        

        mid = len(users) // 2
        left_half = USER.sort_users_by_name(users[:mid])
        right_half = USER.sort_users_by_name(users[mid:])
        

        return USER._merge(left_half, right_half)

    @staticmethod
    def _merge(left, right):
        sorted_list = []
        i = j = 0
        

        while i < len(left) and j < len(right):
            if left[i].name <= right[j].name:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        

        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        
        return sorted_list

    def display_user(self):
        print(f"User ID: {self.user_id}, Name: {self.name}, Email: {self.email}, Age: {self.age}, Bank Balance: ${self.bank_balance}, Debt: ${self.debt}")
if __name__ == "__main__":
    user1 = USER(1, "Alice", "alice@example.com", 30, "2023-01-15", 5000.75, 200.00)
    user2 = USER(2, "Bob", "bob@example.com", 40, "2022-12-10", 3000.50, 500.00)
    user3 = USER(3, "Charlie", "charlie@example.com", 25, "2023-02-20", 1500.25, 100.00)

    users = [user1, user2, user3]

    for user in users:
        user.email_current_balance()

    sorted_users = USER.sort_users_by_name(users)

    print("Users sorted by name:")
    for user in sorted_users:
        user.display_user()
