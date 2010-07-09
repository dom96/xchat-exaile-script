import xchat, sys, dbus
__module_name__ = "Exaile" 
__module_version__ = "1.0" 
__module_description__ = "Exaile now playing script with some other cool features" 

bus = dbus.SessionBus()

def getSongInfo():
  try:
    remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
    iface = dbus.Interface(remote_object, "org.exaile.Exaile")

    if iface.IsPlaying():
      title = iface.GetTrackAttr("title")
      album = iface.GetTrackAttr("album")
      artist = iface.GetTrackAttr("artist")
      pos = iface.CurrentPosition()
      length = iface.GetTrackAttr("__length")
      if length > 0:
          length = '%d:%02d' % (float(length) / 60, float(length) % 60)
      else:
          length = "0:00"
      
      return (title, artist, album, pos, length)
    else:
      return 0
  except dbus.exceptions.DBusException:
    return 1


def printSong(word, word_eol, userdata):
  songInfo = getSongInfo()
  if songInfo == 0:
    xchat.prnt("Exaile is not playing")
  elif songInfo == 1:
    xchat.prnt("Exaile is not running")
  else:
    if not userdata:
      xchat.command("me is listening to %s by %s - %s (%s/%s)" % songInfo)
    else:
      xchat.command("me is listening to \x0303%s\x03 by \x0303%s\x03 - \x0303%s\x03 (\x0305%s\x03/\x0305%s\x03)" % songInfo)
  
  return xchat.EAT_ALL

def printExaileVersion(word, word_eol, userdata):
  try:
    remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
    iface = dbus.Interface(remote_object, "org.exaile.Exaile")

    xchat.command("me is listening to his awesome tunes using Exaile " + str(iface.GetVersion()))
  except dbus.exceptions.DBusException as Err:
    xchat.prnt("An error occured, but xchat crashes when it gets printed.")
    #xchat.prnt(Err.get_dbus_message()) # Unsafe *cough*

def chooseSong(word, word_eol, next):
  try:
    remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
    iface = dbus.Interface(remote_object, "org.exaile.Exaile")

    if next:
      iface.next_track()
    else:
      iface.prev_track()
      
  except dbus.exceptions.DBusException as Err:
    xchat.prnt("An error occured, but xchat crashes when it gets printed.")
    #xchat.prnt(Err.get_dbus_message()) # Unsafe *cough*

xchat.prnt("Exaile script initialized")
xchat.prnt("Use /np to announce the currently played song")
xchat.hook_command("np", printSong, False)
xchat.hook_command("npc", printSong, True)
xchat.hook_command("exaile_ver", printExaileVersion)
#xchat.hook_command("exnext", chooseSong, True)
#xchat.hook_command("exprev", chooseSong, False)

