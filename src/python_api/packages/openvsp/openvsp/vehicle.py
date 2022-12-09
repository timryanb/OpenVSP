import tempfile
from inspect import getmembers, isfunction

from . import vsp

# Define VSPVehicle class
# This class serves as a light wrapper for doing the bookkeeping of different vehicle instances for the user
# This allows multiple independent instances to be used in same Python instance
class VSPVehicle:

    # Add attribute to keep track of which VSPVehicle instance is currently loaded in openvsp
    _current_instance = None

    def __init__(self, file_name=None):
        """
        Initialize class

        :param file_name: vsp3 file name to load on creation
        """
        # Create temporary file to hold VSP model when switching to another vehicle instance
        self._tmp_file = tempfile.NamedTemporaryFile(suffix=".vsp3")
        # Switch openvsp api to current vehicle instance
        self._switch_instance(new_instance=True)
        # Read in vsp3 file if provided
        if file_name is not None:
            self.ReadVSPFile(file_name)
            self._file_name = file_name
        else:
            self._file_name = "Unnamed.vsp3"

    def _save_instance(self):
        """
        Save current work into temporary file
        """
        # Get user-defined file name
        self._file_name = vsp.GetVSPFileName()
        # Write to temporary file to save place
        vsp.WriteVSPFile(self._tmp_file.name)

    def _load_instance(self):
        """
        Load in previous work from temporary file
        """
        # Load previous state from temporary file
        vsp.ReadVSPFile(self._tmp_file.name)
        # Set user-defined file name
        vsp.SetVSP3FileName(self._file_name)

    def _switch_instance(self, new_instance=False):
        """
        Make sure the previous VSPVehicle instance saves its model
        and open this VSPVehicle model in the OpenVSP API

        :param new_instance: Flag to determine if this instance was just created
        :return:
        """
        # Check if the VSPVehicle instance has changed since the last call to the module
        current_instance = self._current_instance
        if current_instance != self:
            # Give the previous VSPVehicle instance a chance to save its work
            if isinstance(current_instance, VSPVehicle):
                current_instance._save_instance()
            # Clear the model
            vsp.ClearVSPModel()
            # If this instance wasn't just created, load in model into the OpenVSP API
            if not new_instance:
                self._load_instance()
            # Update class attribute for current instance with self
            self._set_current_instance(self)

    def __del__(self):
        """
        Do necessary cleanup before class is freed
        """
        # Check if this was the last loaded instance
        if self._current_instance == self:
            # Clear model
            vsp.ClearVSPModel()
            # Remove pointer to self
            self._set_current_instance(None)
        # Close temp file so it can be deleted
        self._tmp_file.close()

    @classmethod
    def _set_current_instance(cls, instance):
        """
        Update current instance attribute of class so all instances know which vehicle is currently loaded

        :param instance: Pointer to last VSPVehicle instance to call openvsp or None
        """
        cls._current_instance = instance

# This function takes in a function from the vsp module
# and wraps it with a _switch_instance call before and after the call
# This will allow our class above to always use the correct Vehicle instance
def wrap_method(original_method):
    def new_method(self, *args, **kwargs):
        self._switch_instance()
        # Call openvsp interface API
        out = original_method(*args, **kwargs)
        # Return output
        return out
    # Return new wrapped method
    return new_method

# Loop through each function in vsp module and add it as a method to VSPVehicle
for member_name, member_func in getmembers(vsp, isfunction):
    setattr(VSPVehicle, member_name, wrap_method(member_func))