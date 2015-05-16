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

/**
 * Converts an HSL color value to RGB. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSL_color_space.
 * Assumes h, s, and l are contained in the set [0, 1] and
 * returns r, g, and b in the set [0, 255].
 *
 * @param   Number  h       The hue
 * @param   Number  s       The saturation
 * @param   Number  l       The lightness
 * @return  Array           The RGB representation
 * http://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion
 */
function hslToRgb(h, s, l){
    var r, g, b;

    if(s == 0){
        r = g = b = l; // achromatic
    }else{
        var hue2rgb = function hue2rgb(p, q, t){
            if(t < 0) t += 1;
            if(t > 1) t -= 1;
            if(t < 1/6) return p + (q - p) * 6 * t;
            if(t < 1/2) return q;
            if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        }

        var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        var p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }

    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
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
// -- deprecated --
// function getRC() {
//   // take a random integer between 85 (0) and 128 (rather than 0 and 255)
//   // then add 127 to make the colour lighter
//   return Math.floor(Math.random() * (128-85) + 85) + 127;
// }

function genColor(idx, l) {
  //return rgbToHex(getRC(), getRC(), getRC());
  return hslToRgb(idx*(1.2)/(2*l) + 0.02,0.65,0.83);
}

// RFC4122 version 4 compliant UUID
function gUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
    return v.toString(16);
  });
}

// These will be later loaded from a separate JSON file, 
// for the moment we manage them by hand here
var apiUrl = "//mathcal-mseri.rhcloud.com";

var categories = [{
    account: '/json/las', 
    label: "London Analysis and Probability Seminar",
    url: "http://www.london-analysis-seminar.org.uk/",
    parser: "flask",
    enabled: true
  },
  {
    account: 'imperial.pure.analysis%40gmail.com', 
    label: "Imperial College Analysis Seminar",
    url: "http://www.imperial.ac.uk/a-z-research/mathematical-analysis/pure-analysis-and-pdes/activities/",
    parser: "gCal",
    enabled: true
  },
  {
    account: 'gkij4q9m1249c2osijddav6dig%40group.calendar.google.com', 
    label: "KCL Analysis Seminar",
    url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/analysis/events/seminars.aspx",
    parser: "gCal",
    enabled: true
  },
  {
    account: 'giu2ael3iq4sd9ucqa2uur7048%40group.calendar.google.com',
    label: "KCL/UCL Geometry Seminar",
    url: "http://www.ucl.ac.uk/geometry/seminars.htm",
    parser: "gCal",
    enabled: true
  },
  {
    account: '/json/nts',
    label: "Number Theory Seminar",
    url: "http://www.homepages.ucl.ac.uk/~ucahsze/seminars.html",
    parser: "flask",
    enabled: true
  },
  {
    account: 'magicseminar%40googlemail.com',
    label: "MAGIC Seminar",
    url: "http://coates.ma.ic.ac.uk/magic/",
    parser: "gCal",
    enabled: true
  },
  {
    account: '84rn4klt27550hfpciblhjb71s%40group.calendar.google.com',
    label: "KCL Disordered System Seminar",
    url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/disorderedsys/seminars.aspx",
    parser: "gCal",
    enabled: true
  },
  {
    account: 'fnmlc1qjb290apdf07h02ut59s%40group.calendar.google.com',
    label: "KCL Theoretical Physics Seminar",
    url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/theorphysics/seminars.aspx",
    parser: "gCal",
    enabled: true
  },
  {
    account: '/json/ic/sas',
    label: "IC Stochastic Analysis Seminar",
    url: "http://www3.imperial.ac.uk/stochasticanalysisgroup/events",
    parser: "flask",
    enabled: true
  },
  {
    account: '/json/ic/taktic',
    label: "TAKTIC: Topology and Knot Theory at Imperial College",
    url: "http://www3.imperial.ac.uk/geometry/seminars/taktic",
    parser: "flask",
    enabled: true
  },
  {
    account: '/json/ic/apde',
    label: "IC Applied PDEs Seminars",
    url: "http://www3.imperial.ac.uk/ammp/aboutammp/pdesseminars",
    parser: "flask",
    enabled: true
  },
  {
    account: '/json/ic/ammp',
    label: "IC Applied Mathematics and Mathematical Physics Seminar",
    url: "http://www3.imperial.ac.uk/ammp/aboutammp/ammpseminar",
    parser: "flask",
    enabled: true
  },
  {
    account: '/json/ic/fd',
    label: "IC Fluid dynamics group seminar",
    url: "http://www3.imperial.ac.uk/ammpfluiddynamics/seminars",
    parser: "flask",
    enabled: true
  },
  {
    account: '/json/ic/ftmp',
    label: "IC fortnightly seminar on topics in Mathematical Physics",
    url: "http://www3.imperial.ac.uk/mathematicalphysics/events",
    parser: "flask",
    enabled: true
  },
  {
    account: '/json/ic/ip', 
    label: "Imperial Probability Centre",
    url: "http://wwwf.imperial.ac.uk/~amijatov/IP/index.php",
    parser: "flask",
    enabled: true
  }
];

// Generate the colors in a "rainbow" fashion
for (var i=0; i<categories.length; i++) {
  categories[i].id = gUUID(),
  categories[i].color = rgbToHex.apply(this, genColor(i, categories.length));
}

$(document).ready(function() {

  // Get basic JSON feed from Google Calendar
  // or our Flask App
  function getJSON(category) {
    var url;
    if (category.parser == "gCal") {
      url = 'https://www.google.com/calendar/feeds/' + category.account +'/public/basic?alt=json&hl=en';
    } else {
      url = apiUrl + category.account;
    }

    return $.getJSON(url).done(function(data) {
         listEvents(data, category);
       });
  }

  function listEvents(root, category) {
    var entries;
    if (category.parser == "gCal") {
      var feed = root.feed;
      entries = feed.entry || [];
    } else {
      entries = root;
    }

    var events = entries.map(getEventWith(category)).filter(isNotNull);

    $('#calendar').fullCalendar( 'addEventSource', { events:events, cid: category.id } );
    $('#calendar').fullCalendar( 'refetchEvents' );

    var spinner = "#" + category.id + " .spinner";
    $(spinner).remove();
  }

  function isNotNull(element) {
    return element != null;
  }

  // generate getEvent function to elaborate the entries from the
  // JSON feeds
  // we use the closure to keep lin 107 shorter and more readable
  function getEventWith(category) {
    return function getEvent(entry) {
      if (category.parser == "gCal"){
        return getGCalEvent(entry, category);
      }

      return getFlaskEvent(entry, category);
    };
  }

  // build the events out of Google calendar's feed entries
  // (it uses horrible hacked regex parsing of the content to extract and 
  // re-elaborate the data)
  function getGCalEvent(entry, category) {
    // this is easy, just get title and content
    var title = (entry.title.type == 'html') ? entry.title.$t : escape(entry.title.$t);

    //Workaround for duplicate London Analysis Seminar from Imperial Analysis calendar
    if (title.slice(0,4) == "LANS") {
      return null;
    }
    if (title.indexOf("London Analysis and Probability Seminar") > -1) {
      return null;
    }

    var content = (entry.content.type == 'html') ? entry.content.$t : escape(entry.content.$t);

    // Get When and Where from the formatted content in the google calendar string
    var strippedContent = content.replace(/(<br \/>|\n)/g,'§');
    var wAndWRegex = /When: (\w{3} \w{3} \d+, \d{4} \d+:?\d*[ap]m) to (.*\d+:?\d*[ap]m).*Where: ([^§]*)§+.*/;
    var whenAndWhere = wAndWRegex.exec(strippedContent);

    var descRegex = /.*Event Description: (.*)/;
    var description = descRegex.exec(strippedContent);

    // whenAndWhere infos are essential. If something went wrong with
    // them we are not going to process the event
    if (whenAndWhere) {
      // get rid of the original string (strippedContent)
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

      if (description) {
        description = description[1].replace(/§/g,'<br />');
      }

      return {
        title: title, 
        start: start, 
        end: stop,
        where: where,
        content: description, 
        category: category.label,
        categoryurl: category.url,
        backgroundColor: category.color,
        borderColor: lightenDarkenColor(category.color, -42),
        textColor: lightenDarkenColor(category.color, -112),
        allDay: false
      };
    }

    return null;
  }

  // build the event out of our nice flask-scraped-and-generated json
  function getFlaskEvent(entry, category) {
    return {
        title: entry.title, 
        start: new Date(entry.start), 
        end: new Date(entry.end),
        where: entry.location,
        content: entry.description, 
        category: category.label,
        categoryurl: category.url,
        backgroundColor: category.color,
        borderColor: lightenDarkenColor(category.color, -42),
        textColor: lightenDarkenColor(category.color, -112),
        allDay: false
      };
  }

  // style and generate the legenda for a category
  function styleCategory(category) {
    var item = [
      '<li id="',
      category.id,
      '" style="border-color:',
      lightenDarkenColor(category.color, -42),
      '; background-color:',
      category.color,
      // ';"><input type="checkbox" checked="',
      // category.enabled
      // ,'"/> <a style="text-decoration: none; color:', 
      ';"><a style="text-decoration: none; color:', 
      lightenDarkenColor(category.color, -112),
      ';" href="',
      category.url,
      '" target="_blank">',
      category.label,
      addSpinner(category.enabled),
      '</li>\n'
      ];
    return item.join("");
  }

  function addSpinner(isEnabled) {
    if (isEnabled) {
      return '<div class="spinner"></div>'
    } else {
      return ''
    }
  }

  // generate categories legend
  function generateLegend(categories) {
    var legend = ['<h2 id="legendTitle">Colours Legend</h2><ul>'];
    legend = legend.concat(categories.map(styleCategory));
    legend.push('</ul>');

    $('#legend').html("");
    $('#legend').html(legend.join(""));
  }

  function populateCalendar() {
    //$('#calendar').fullCalendar( 'removeEvents' );
    generateLegend(categories);
    categories.filter(entryEnabled).map(getJSON);
  }

  function entryEnabled(category){
    return category.enabled;
  }

  // execute scraping and elaborations
  // cross fingers and wait a little
  populateCalendar();

  // $("ul li input").bind("click", function() {
  //   var ele = $(this)[0];
  //   var cid = ele.parentNode.parentNode.id;
  //   for(var i=0; i<categories.length; i++) {
  //       if (categories[i].id == cid) {
  //         categories[i].enabled = ele.checked;
  //       }
  //   }

  //   populateCalendar();
  // });

});
