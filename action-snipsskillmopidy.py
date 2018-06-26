+# -*-: coding utf-8 -*-
+
+import ConfigParser
+from hermes_python.hermes import Hermes
+from hermes_python.ontology import *
+import io
+
+from snipsmopidy.snipsmopidy import SnipsMopidy
+
+CONFIGURATION_ENCODING_FORMAT = "utf-8"
+CONFIG_INI = "config.ini"
+
+HOSTNAME = "localhost"
+
+HERMES_HOST = "{}:1883".format(HOSTNAME)
+MOPIDY_HOST = HOSTNAME
+
+class SnipsConfigParser(ConfigParser.SafeConfigParser):
+    def to_dict(self):
+        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}
+
+
+def read_configuration_file(configuration_file):
+    try:
+        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
+            conf_parser = SnipsConfigParser()
+            conf_parser.readfp(f)
+            return conf_parser.to_dict()
+    except (IOError, ConfigParser.Error) as e:
+        return dict()
+
+def addSong_callback(hermes, intentMessage):
+    pass
+
+def getInfos_callback(hermes, intentMessage):
+    tts_sentence = "This is {} by {} on the album {}".format(*hermes.skill.get_info())
+    hermes.publish_end_session(intentMessage.session_id, tts_sentence)
+
+def nextSong_callback(hermes, intentMessage):
+    hermes.skill.next_song()
+
+def playAlbum_callback(hermes, intentMessage):
+    if len(intentMessage.slots.album_name):
+        album_name = intentMessage.slots.album_name.first().value
+        hermes.skill.play_album(album_name, shuffle=(
+                    len(intentMessage.slots.album_lecture_mode) and intentMessage.slots.album_lecture_mode.first().value == "shuffle"))
+
+
+def playArtist_callback(hermes, intentMessage):
+    if len(intentMessage.slots.artist_name):
+        artist_name = intentMessage.slots.artist_name.first().value
+        hermes.skill.play_artist(artist_name)
+
+def playPlaylist_callback(hermes, intentMessage):
+    if len(intentMessage.slots.playlist_name):
+        playlist_name = intentMessage.slots.playlist_name.first().value
+        hermes.skill.play_playlist(playlist_name, shuffle=(
+                    len(intentMessage.slots.playlist_lecture_mode) and intentMessage.slots.playlist_lecture_mode.first().value == "shuffle"))
+
+
+def playSong_callback(hermes, intentMessage):
+    if len(intentMessage.slots.song_name):
+        hermes.skill.play_song(intentMessage.slots.song_name.first().value)
+
+def previousSong_callback(hermes, intentMessage):
+    hermes.skill.previous_song()
+
+def radioOn_callback(hermes, intentMessage):
+    pass
+
+def resumeMusic_callback(hermes, intentMessage):
+    hermes.skill.play()
+
+def speakerInterrupt_callback(hermes, intentMessage):
+    hermes.skill.pause()
+
+def volumeDown_callback(hermes, intentMessage):
+    if len(intentMessage.slots.volume_lower):
+        volume_lower = intentMessage.slots.volume_lower.first().value
+        hermes.skill.volume_down(volume_lower)
+    else:
+        hermes.skill.volume_down(None)
+
+def volumeUp_callback(hermes, intentMessage):
+    hermes.skill.set_to_previous_volume()
+    if len(intentMessage.slots.volume_lower):
+        volume_lower = intentMessage.slots.volume_lower.first().value
+        hermes.skill.volume_down(volume_lower)
+    else:
+        hermes.skill.volume_down(None)
+
+
+if __name__ == "__main__":
+
+    with Hermes(HERMES_HOST) as h:
+
+        h.skill = SnipsMopidy(MOPIDY_HOST)
+
+        h\
+            .subscribe_intent("volumeUp", volumeUp_callback) \
+            .subscribe_intent("previousSong", previousSong_callback) \
+            .subscribe_intent("playSong", playSong_callback) \
+            .subscribe_intent("playArtist", playArtist_callback) \
+            .subscribe_intent("getInfos", getInfos_callback) \
+            .subscribe_intent("speakerInterrupt", speakerInterrupt_callback) \
+            .subscribe_intent("resumeMusic", resumeMusic_callback) \
+            .subscribe_intent("addSong", addSong_callback) \
+            .subscribe_intent("nextSong", nextSong_callback) \
+            .subscribe_intent("radioOn", radioOn_callback) \
+            .subscribe_intent("playAlbum", playAlbum_callback) \
+            .subscribe_intent("volumeDown", volumeDown_callback) \
+            .subscribe_intent("playPlaylist", playPlaylist_callback) \
+            .loop_forever()
