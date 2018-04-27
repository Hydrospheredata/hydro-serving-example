import os

from tensorflow.core.protobuf import saver_pb2
from tensorflow.python.lib.io import file_io
from tensorflow.python.ops import variables
from tensorflow.python.saved_model import constants
from tensorflow.python.saved_model.builder_impl import SavedModelBuilder
from tensorflow.python.training import saver as tf_saver
from tensorflow.python.util import compat


class StatefulSavedModelBuilder(SavedModelBuilder):
    STATE_ZERO_COLLECTION_KEY = "h_zero_states"
    STATE_PLACEHOLDERS_COLLECTION_KEY = "h_state_placeholders"

    def add_meta_graph_and_variables(self, sess, tags, signature_def_map=None, assets_collection=None,
                                     legacy_init_op=None, clear_devices=False, main_op=None, strip_default_attrs=False):
        # pylint: disable=line-too-long
        """Adds the current meta graph to the SavedModel and saves variables.

        Creates a Saver to save the variables from the provided session. Exports the
        corresponding meta graph def. This function assumes that the variables to be
        saved have been initialized. For a given `SavedModelBuilder`, this API must
        be called exactly once and for the first meta graph to save. For subsequent
        meta graph defs to be added, the `add_meta_graph()` API must be used.

        Args:
          sess: The TensorFlow session from which to save the meta graph and
            variables.
          tags: The set of tags with which to save the meta graph.
          signature_def_map: The map of signature def map to add to the meta graph
            def.
          assets_collection: Assets collection to be saved with SavedModel.
          legacy_init_op: Legacy support for op or group of ops to execute after the
              restore op upon a load.
          clear_devices: Set to true if the device info on the default graph should
              be cleared.
          main_op: Op or group of ops to execute when the graph is loaded. Note
              that when the main_op is specified it is run after the restore op at
              load-time.
          strip_default_attrs: Boolean. If `True`, default-valued attributes will be
            removed from the NodeDefs. For a detailed guide, see
            [Stripping Default-Valued Attributes](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/saved_model/README.md#stripping-default-valued-attributes).
        """
        # pylint: enable=line-too-long
        if self._has_saved_variables:
            raise AssertionError("Graph state including variables and assets has "
                                 "already been saved. Please invoke "
                                 "`add_meta_graph()` instead.")

        # Validate the signature def map to ensure all included TensorInfos are
        # properly populated.
        self._validate_signature_def_map(signature_def_map)

        # Save asset files and write them to disk, if any.
        self._save_and_write_assets(assets_collection)

        # Create the variables sub-directory, if it does not exist.
        variables_dir = os.path.join(
            compat.as_text(self._export_dir),
            compat.as_text(constants.VARIABLES_DIRECTORY))
        if not file_io.file_exists(variables_dir):
            file_io.recursive_create_dir(variables_dir)

        variables_path = os.path.join(
            compat.as_text(variables_dir),
            compat.as_text(constants.VARIABLES_FILENAME))

        if main_op is None:
            # Add legacy init op to the SavedModel.
            self._maybe_add_legacy_init_op(legacy_init_op)
        else:
            self._add_main_op(main_op)

        # Initialize a saver to generate a sharded output for all saveables in the
        # current scope.
        saver = tf_saver.Saver(
            variables._all_saveable_objects(),  # pylint: disable=protected-access
            sharded=True,
            write_version=saver_pb2.SaverDef.V2,
            allow_empty=True)

        # Save the variables. Also, disable writing the checkpoint state proto. The
        # file is not used during SavedModel loading. In addition, since a
        # SavedModel can be copied or moved, this avoids the checkpoint state to
        # become outdated.
        saver.save(sess, variables_path, write_meta_graph=False, write_state=False)

        print(sess.graph.get_collection(StatefulSavedModelBuilder.STATE_ZERO_COLLECTION_KEY))
        print(sess.graph.get_collection(StatefulSavedModelBuilder.STATE_PLACEHOLDERS_COLLECTION_KEY))

        # Export the meta graph def.

        # The graph almost certainly previously contained at least one Saver, and
        # possibly several (e.g. one for loading a pretrained embedding, and another
        # for the model weights).  However, a *new* Saver was just created that
        # includes all of the variables.  Removing the preexisting ones was the
        # motivation for the clear_extraneous_savers option, but it turns out that
        # there are edge cases where that option breaks the graph.  Until that is
        # resolved, we just leave the option set to False for now.
        # TODO(soergel): Reinstate clear_extraneous_savers=True when possible.
        meta_graph_def = saver.export_meta_graph(
            clear_devices=clear_devices,
            collection_list=[
                StatefulSavedModelBuilder.STATE_ZERO_COLLECTION_KEY,
                StatefulSavedModelBuilder.STATE_PLACEHOLDERS_COLLECTION_KEY
            ],
            strip_default_attrs=strip_default_attrs
        )

        # Tag the meta graph def and add it to the SavedModel.
        self._tag_and_add_meta_graph(meta_graph_def, tags, signature_def_map)

        # Mark this instance of SavedModel as having saved variables, such that
        # subsequent attempts to save variables will fail.
        self._has_saved_variables = True

    def add_meta_graph(self, tags, signature_def_map=None, assets_collection=None, legacy_init_op=None,
                       clear_devices=False, main_op=None, strip_default_attrs=False):
        # pylint: disable=line-too-long
        """Adds the current meta graph to the SavedModel.

        Creates a Saver in the current scope and uses the Saver to export the meta
        graph def. Invoking this API requires the `add_meta_graph_and_variables()`
        API to have been invoked before.

        Args:
          tags: The set of tags to annotate the meta graph def with.
          signature_def_map: The map of signature defs to be added to the meta graph
              def.
          assets_collection: Assets collection to be saved with SavedModel. Note
              that this collection should be a subset of the assets saved as part of
              the first meta graph in the SavedModel.
          legacy_init_op: Legacy support for op or group of ops to execute after the
              restore op upon a load.
          clear_devices: Set to true if the device info on the default graph should
              be cleared.
          main_op: Op or group of ops to execute when the graph is loaded. Note
              that when the main_op is specified it is run after the restore op at
              load-time.
          strip_default_attrs: Boolean. If `True`, default-valued attributes will be
            removed from the NodeDefs. For a detailed guide, see
            [Stripping Default-Valued Attributes](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/saved_model/README.md#stripping-default-valued-attributes).

        Raises:
          AssertionError: If the variables for the SavedModel have not been saved
              yet, or if the graph already contains one or more legacy init ops.
        """
        # pylint: enable=line-too-long
        if not self._has_saved_variables:
            raise AssertionError(
                "Graph state including variables and assets has not been saved yet. "
                "Please invoke `add_meta_graph_and_variables()` first.")

        # Validate the signature def map to ensure all included TensorInfos are
        # properly populated.
        self._validate_signature_def_map(signature_def_map)

        # Save asset files and write them to disk, if any.
        self._save_and_write_assets(assets_collection)

        if main_op is None:
            # Add legacy init op to the SavedModel.
            self._maybe_add_legacy_init_op(legacy_init_op)
        else:
            self._add_main_op(main_op)

            # Initialize a saver to generate a sharded output for all saveables in the
        # current scope.
        saver = tf_saver.Saver(
            variables._all_saveable_objects(),  # pylint: disable=protected-access
            sharded=True,
            write_version=saver_pb2.SaverDef.V2,
            allow_empty=True)

        # The graph almost certainly previously contained at least one Saver, and
        # possibly several (e.g. one for loading a pretrained embedding, and another
        # for the model weights).  However, a *new* Saver was just created that
        # includes all of the variables.  Removing the preexisting ones was the
        # motivation for the clear_extraneous_savers option, but it turns out that
        # there are edge cases where that option breaks the graph.  Until that is
        # resolved, we just leave the option set to False for now.
        # TODO(soergel): Reinstate clear_extraneous_savers=True when possible.
        meta_graph_def = saver.export_meta_graph(
            clear_devices=clear_devices,
            collection_list=[
                StatefulSavedModelBuilder.STATE_ZERO_COLLECTION_KEY,
                StatefulSavedModelBuilder.STATE_PLACEHOLDERS_COLLECTION_KEY
            ],
            strip_default_attrs=strip_default_attrs
        )

        # Tag the meta graph def and add it to the SavedModel.
        self._tag_and_add_meta_graph(meta_graph_def, tags, signature_def_map)
