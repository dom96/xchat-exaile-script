import xchat, sys, dbus
__module_name__ = "Exaile" 
__module_version__ = "1.0" 
__module_description__ = "Exaile now playing script with some other cool features" 

def getSongInfo():
  bus = dbus.SessionBus()
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



xchat.prnt("Exaile script initialized")
xchat.prnt("Use /np to announce the currently played song")
xchat.hook_command("np", printSong, False)
xchat.hook_command("npc", printSong, True)

