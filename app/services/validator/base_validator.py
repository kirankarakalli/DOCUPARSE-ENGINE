

class BaseValidator:
    def validate(self,data:dict):
        raise NotImplementedError("Validator must implement validate method")
