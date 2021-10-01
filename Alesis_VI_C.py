# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.10 (default, Jun  2 2021, 10:49:15) 
# [GCC 9.4.0]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Alesis_VI\Alesis_VI.py
# Compiled at: 2021-09-02 03:33:28
# Size of source mod 2**32: 2578 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Layer import Layer
from _Framework.MidiMap import make_encoder, make_button, MidiMap as MidiMapBase
from _Framework.MixerComponent import MixerComponent
from _Framework.TransportComponent import TransportComponent
import Live

class MidiMap(MidiMapBase):

    def __init__(self, *a, **k):
        (super(MidiMap, self).__init__)(*a, **k)
        self.add_momentary_button('Stop', 0, 118, MIDI_CC_TYPE)
        self.add_momentary_button('Play', 0, 119, MIDI_CC_TYPE)
        self.add_momentary_button('Loop', 0, 115, MIDI_CC_TYPE)
        self.add_momentary_button('Record', 0, 114, MIDI_CC_TYPE)
        self.add_momentary_button('Forward', 0, 117, MIDI_CC_TYPE)
        self.add_momentary_button('Backward', 0, 116, MIDI_CC_TYPE)
        # There are extra values here for the Alesis VI61 which has 16 knobs
        # the VI25 I'm using only has 8 knobs, 20-27
        # I use Preset2 and put the knobs on channel 2 (but it is 0 indexed)

        self.add_matrix('Volume_Encoders', make_encoder, 1, [
         list(range(20, 32)) + [35, 41, 46, 47]], MIDI_CC_TYPE)


    def add_momentary_button(self, name, channel, number, midi_message_type):
        self[name] = ButtonElement(True, midi_message_type, channel, number, name=name)


class Alesis_VI_C(ControlSurface):

    def __init__(self, *a, **k):
        (super(Alesis_VI_C, self).__init__)(*a, **k)
        with self.component_guard():
            midimap = MidiMap()
            transport = TransportComponent(name='Transport',
              is_enabled=False,
              layer=Layer(play_button=(midimap['Play']),
              stop_button=(midimap['Stop']),
              loop_button=(midimap['Loop']),
              record_button=(midimap['Record']),
              seek_forward_button=(midimap['Forward']),
              seek_backward_button=(midimap['Backward'])))
            
            self._mute_buttons = ButtonMatrixElement(rows=[[ make_button(u'Mute_Button_%d' % (index + 1,), 0, 48+index, MIDI_CC_TYPE) for index in range(8) ]], name=u'Mute_Buttons')
            self._solo_buttons = ButtonMatrixElement(rows=[[ make_button(u'Solo_Button_%d' % (index + 1,), 0, 56+index, MIDI_CC_TYPE) for index in range(8) ]], name=u'Solo_Buttons')
            self._arm_buttons = ButtonMatrixElement(rows=[[ make_button(u'Arm_Button_%d' % (index + 1,), 0, 64+index, MIDI_CC_TYPE) for index in range(8) ]], name=u'Arm_Buttons')

            mixer_size = len(midimap['Volume_Encoders'])
            self._mixer = MixerComponent(mixer_size,
              name='Mixer',
              is_enabled=False,
              layer=Layer(volume_controls=midimap['Volume_Encoders'],
                          mute_buttons=self._mute_buttons,
                          solo_buttons=self._solo_buttons,
                          arm_buttons=self._arm_buttons))
            transport.set_enabled(True)
            self._mixer.set_enabled(True)

            # Mapping the Knobs to active device on channel 1 (which is my default Preset 1)
            encoders = ButtonMatrixElement(rows=[[ EncoderElement(MIDI_CC_TYPE, 0, identifier + 20, Live.MidiMap.MapMode.absolute, name=u'Encoder_%d' % identifier) for identifier in range(8) ]])
            self._device = DeviceComponent(name=u'Device', is_enabled=False, layer=Layer(parameter_controls=encoders), device_selection_follows_track_selection=True)
            self._device.set_enabled(True)
            self.set_device_component(self._device)
    
# okay decompiling ./Alesis_VI.pyc
