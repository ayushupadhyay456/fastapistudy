class Email:
    def __init__(self):
        self.errors=[]
        self.names=['Ayush','Somay']

    def email_validator(self,email):
        if '@' not in email:
            self.errors.append("Email not Coorect")
            return False
        else:
            return True
    def username_taken(self,username):
        if username in self.names:
           self.errors.append("Username Already Taken")
           return self.errors
        else:
             self.errors.append("Welcome")
             return self.errors
    @staticmethod
    def hello_get():
        return 5*3
    def get_errors(self):
        return self.errors

user1=Email()

if user1.email_validator(email='ayush@gmail.com')==False:
    print(user1.get_errors())
print(user1.username_taken(username="Rahul"))
print(Email.hello_get())

    
