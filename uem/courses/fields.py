from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    """
    Custom Django field to manage the order of related objects.

    This field is intended to be used in models that require a specific 
    ordering of instances. It automatically assigns an order value to new 
    instances based on the current maximum order of existing instances 
    related by specified fields.
    """
    
    def __init__(self, for_fields=None, *args, **kwargs):
        """
        Initialize the OrderField.

        Parameters:
        for_fields (list): A list of field names that this field should 
                           consider when determining the order. 
        """
        self.for_fields = for_fields  # Store the fields to filter by
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Assign an order value before saving the model instance.

        This method checks if the order value is currently set. If not,
        it calculates the new order value based on existing instances 
        and assigns it to the instance.

        Parameters:
        model_instance: The instance of the model being saved.
        add (bool): Indicates if this is a new instance being added.

        Returns:
        int: The assigned order value.
        """
        if getattr(model_instance, self.attname) is None:
            # No current value; calculate the new order value
            try:
                qs = self.model.objects.all()  # Query all instances
                if self.for_fields:
                    # Filter by objects with the same field values
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                
                # Get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0  # If no existing item, start at 0

            setattr(model_instance, self.attname, value)  # Assign the new order value
            return value  # Return the assigned value
        else:
            return super().pre_save(model_instance, add)  # Call the parent's pre_save method for existing values
