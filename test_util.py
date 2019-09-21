class MockPhotoCtrl:
    path = None
    name = None

    def init(self, path, name):
        self.path = path
        self.name = name

    def make_photo(self):
        return True, self.name
        

    def get_path(self, phid):
        return self.path, phid + ".jpg"


class MockMotorCtrl:


    def fwd_on(self):
        return True

    def fwd_off(self):
        return True

    def back_on(self):
        return True

    def back_off(self):
        return True

    def right_on(self):
        return True

    def right_off(self):
        return True

    def left_on(self):
        return True

    def left_off(self):
        return True
