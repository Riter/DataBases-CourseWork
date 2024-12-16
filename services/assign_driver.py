from repositories.assign_driver import call_assign_drivers

class AssignDriverService:
    def __init__(self):
        pass

    def assign_drivers(self) -> str:
        """
        Call the stored procedure to assign drivers to routes automatically.

        Returns:
            str: Result message indicating success or any errors.
        """
        call_assign_drivers()
