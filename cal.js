'use strict'

// Pastel Color Palette generation
// it simply generates random pastel coluors, with no attempt to 
// stick to triads or other principles (yet).
// credits: blog.functionalfun.net/2008/07/random-pastel-colour-generator.html
//          stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
//          http://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors

function rgbToHex(red, green, blue) {
    return "#" + ((1 << 24) + (red << 16) + (green << 8) + blue).toString(16).slice(1);
}

// takes a HEX coluor and add the provided amount to each component
// use negatives to darken and do not exaggerate

function lightenDarkenColor(col, amt) {
  // we use slice to get rid of the # in front of the colour
  var num = parseInt(col.slice(1),16);
  var r = (num >> 16) + amt;
  var b = ((num >> 8) & 0x00FF) + amt;
  var g = (num & 0x0000FF) + amt;
  return rgbToHex(r, g, b);
}

function darken(col) {
  return lightenDarkenColor(col, -42);
}

// was getRandomComponent but I'm lazy
function getRC() {
  // take a random integer between 85 (0) and 128 (rather than 0 and 255)
  // then add 127 to make the colour lighter
  return Math.floor(Math.random() * (128-85) + 85) + 127;
}

function genColor() {
  return rgbToHex(getRC(), getRC(), getRC());
}


// These will be later loaded from a separate JSON file, 
// for the moment we manage them by hand here
// TODO: add url property
var categories = [{
    account: 'imperial.pure.analysis%40gmail.com', 
    label: "Imperial College Analysis Seminar",
    color: genColor()
  },
  {
    account: 'gkij4q9m1249c2osijddav6dig%40group.calendar.google.com', 
    label: "KCL Analysis Seminar",
    color: genColor()
  },
  {
    account: 'giu2ael3iq4sd9ucqa2uur7048%40group.calendar.google.com',
    label: "KCL and UCL Geometry Seminar",
    color: genColor()
}];


$(document).ready(function() {

  // Get basic JSON feed from Google Calendar
  function getGoogleJSON(category) {
    return $.getJSON( 'https://www.google.com/calendar/feeds/' + category.account +'/public/basic?alt=json&hl=en').done(function(data) {
         listEvents(data, category);
       });
  }

  function listEvents(root, category) {
    var feed = root.feed;
    var entries = feed.entry || [];

    var events = entries.map(getEventWithCategory(category)).filter(isNull);

    $('#calendar').fullCalendar( 'addEventSource', events);
    $('#calendar').fullCalendar( 'refetchEvents' );
  }

  function isNull(element) {
    return element != null;
  }

  // build the vent out of google's calendar feed entries
  // it uses horrible hacked regex parsing of the content to extract and 
  // re-elaborate the data
  function getEventWithCategory(category){
    return function getEvent(entry) {
      // this is easy, just get title and content
      var title = (entry.title.type == 'html') ? entry.title.$t : escape(entry.title.$t);
      var content = (entry.content.type == 'html') ? entry.content.$t : escape(entry.content.$t);

      // Get When and Where from the formatted content in the google calendar string
      // TODO: Extract description if present
      var wAndWStr = content.replace(/(<br \/>|\n)/g,';');
      var wAndWRegex = /When: (\w{3} \w{3} \d+, \d{4} \d+:?\d*[ap]m) to (.*\d+:?\d*[ap]m).*Where: ([^;]*);+.*/;
      var whenAndWhere = wAndWRegex.exec(wAndWStr);

      if (whenAndWhere) {
        // get rid of the original string (wAndWStr)
        whenAndWhere = whenAndWhere.splice(1);

        // fix start and stop datetime format
        // get (\d\d?)([ap]m) and make into $1:00 $2
        var start = new Date(
          whenAndWhere[0].replace(/([ap]m)/, " $1").replace(/ (\d\d?) /," $1:00 ")
          );

        // add day in fron of stop and fix the time
        // FIXME: I am assuming start/stop in the same day
        var stop = new Date(
          whenAndWhere[0].replace(/\d\d?:?\d?\d?\s?[ap]m/, whenAndWhere[1]).replace(/([ap]m)/, " $1").replace(/ (\d\d?) /," $1:00 ")
          );

        var where = whenAndWhere[2];

        return {
          title: title, 
          start: start, 
          end: stop,
          content: content,
          category: category.label,
          backgroundColor: category.color,
          borderColor: lightenDarkenColor(category.color, -42),
          textColor: lightenDarkenColor(category.color, -105),
          allDay: false
        };
      }

      return null;
    };
  }

  function styleCategory(category) {
    var item = [
      '<li style="color:', 
      lightenDarkenColor(category.color, -105),
      '; border-color:',
      lightenDarkenColor(category.color, -42),
      '; background-color:',
      category.color,
      ';">',
      category.label,
      '</li>\n'
      ];
    return item.join("");
  }

  // generate categories legend
  function generateLegend(categories) {
    var html = ['<ul>'];
    html = html.concat(categories.map(styleCategory));
    html.push('</ul>');

    $('#legend').append(html.join(""));
  }

  // execute scraping and elaborations
  // cross fingers and wait a little
  categories.map(getGoogleJSON);
  generateLegend(categories);
});