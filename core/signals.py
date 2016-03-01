from django.dispatch import Signal


# Dataset
dataset_changed = Signal(providing_args=['id'])
dataset_unpublished = Signal(providing_args=['id'])
dataset_removed = Signal(providing_args=['id', 'rev_id'])
dataset_rev_removed = Signal(providing_args=['id'])

# Datastream
datastream_changed = Signal(providing_args=['id'])
datastream_unpublished = Signal(providing_args=['id'])
datastream_removed = Signal(providing_args=['id', 'rev_id'])
datastream_rev_removed = Signal(providing_args=['id'])

# Visualization
visualization_changed = Signal(providing_args=['id'])
visualization_unpublished = Signal(providing_args=['id'])
visualization_removed = Signal(providing_args=['id', 'rev_id'])
visualization_rev_removed = Signal(providing_args=['id'])
