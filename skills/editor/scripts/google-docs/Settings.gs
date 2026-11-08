/**
 * Settings: the only file you edit by hand.
 *
 * Every other file in this project reads these values. Fill them in once.
 *
 * To find a folder ID, open the folder in Google Drive and copy the part of the address after
 * "/folders/". For https://drive.google.com/drive/folders/1AbCdEfGh the ID is 1AbCdEfGh.
 */

var EDITOR_SETTINGS = {
  // The folder that holds your chapter Docs.
  chaptersFolderId: 'PASTE_THE_CHAPTERS_FOLDER_ID_HERE',

  // The folder backups go into. Every Doc is copied here, with a timestamp in its name,
  // before a script changes it.
  backupsFolderId: 'PASTE_THE_BACKUPS_FOLDER_ID_HERE',

  // The folder your images live in (only needed for the Images tools).
  imagesFolderId: 'PASTE_THE_IMAGES_FOLDER_ID_HERE',

  // Your time zone, used in backup names. A list of names is at
  // https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
  timeZone: 'America/New_York',

  // The lines that mark where a chapter starts and ends inside a Doc. Anything outside them
  // (notes, outlines, old drafts) is never changed or counted. Leave both as '' if your Docs
  // hold only the chapter.
  startMarker: '[START CHAPTER]',
  endMarker: '[END CHAPTER]',

  // Width of inserted images, in centimeters.
  imageWidthCentimeters: 15
};
