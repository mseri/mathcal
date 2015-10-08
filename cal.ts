/// <reference path="typings/tsd.d.ts" />

/*
*
*   Pastel Color Palette generation
*
*/

function rgbToHex(red: number, green: number, blue: number): string {
  // credits: stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
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
function hslToRgb(h: number, s: number, l: number): [number, number, number] {
  var r: number, g: number, b: number;

  if (s == 0) {
    r = g = b = l; // achromatic
  } else {
    var hue2rgb = function hue2rgb(p, q, t) {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    }

    var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    var p = 2 * l - q;
    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }

  return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}


// Generates pastel colours whose hue is proportional to idx/l.
// If l is the length of our datastructure and idx its index,
// the colours will be picked progressively forming a rainbow.
// Saturation and luminace have been chosen by trial and error.
function genColor(idx: number, l: number) {
  var rgb = hslToRgb(idx * (1.2) / (2 * l) + 0.02, 0.65, 0.83);
  return rgbToHex.apply(this, rgb);
}


// Takes a HEX coluor and add the provided amount to each component.
// Use negative numbers to darken (do not exaggerate).
// credits: http://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
function lightenDarkenColor(col: string, amt: number): string {
  // we use slice to get rid of the # in front of the colour
  var num = parseInt(col.slice(1), 16);
  var r = (num >> 16) + amt;
  var b = ((num >> 8) & 0x00FF) + amt;
  var g = (num & 0x0000FF) + amt;
  return rgbToHex(r, g, b);
}

function darken(col: string): string {
  return lightenDarkenColor(col, -42);
}


/*
*
*   Seminars data configuration, types and helpers
*
*/

// RFC4122 version 4 compliant UUID generator.
function gUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}


// TODO: These will be later loaded from a separate JSON file, 
// for the moment we manage them by hand here.
var apiUrl = "//mathcal-mseri.rhcloud.com";


// Id, color and enabled are optional only because we want to
// generate them dynamically at runtime.
// TODO: - automatically generate the structure from a JSON or YAML file.
//       - Do classes with auto id/color generation make more sense here?
interface ISeminarData {
  id?: string;
  color?: string;
  account: string;
  label: string;
  url: string;
  enabled?: boolean;
}

interface Event {
  title: string;
  start: Date;
  end: Date;
  where: string;
  content: string;
  category: string;
  categoryUrl: string;
  backgroundColor: string;
  borderColor: string;
  textColor: string;
  allDay: boolean;
}

var seminars_: ISeminarData[] = [
  {
    account: '/json/las',
    label: "London Analysis and Probability Seminar",
    url: "http://www.london-analysis-seminar.org.uk/"
  },
  {
    account: '/json/gcal/imperial.pure.analysis%40gmail.com',
    label: "Imperial College Analysis Seminar",
    url: "http://www.imperial.ac.uk/a-z-research/mathematical-analysis/pure-analysis-and-pdes/activities/"  
   },
  {
    account: '/json/gcal/gkij4q9m1249c2osijddav6dig%40group.calendar.google.com',
    label: "KCL Analysis Seminar",
    url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/analysis/events/seminars.aspx"  
  },
  {
    account: '/json/ic/ipc',
    label: "Imperial Probability Centre",
    url: "http://wwwf.imperial.ac.uk/~amijatov/IP/index.php"
  },
  {
    account: '/json/nts',
    label: "Number Theory Seminar",
    url: "http://www.homepages.ucl.ac.uk/~ucahsze/seminars.html"
  },
  {
    account: '/json/gcal/giu2ael3iq4sd9ucqa2uur7048%40group.calendar.google.com',
    label: "KCL/UCL Geometry Seminar",
    url: "http://www.ucl.ac.uk/geometry/seminars.htm"
  },
  {
    account: '/json/gcal/magicseminar%40googlemail.com',
    label: "MAGIC Seminar",
    url: "http://coates.ma.ic.ac.uk/magic/"
  },
  {
    account: '/json/ic/taktic',
    label: "TAKTIC: Topology and Knot Theory at Imperial College",
    url: "http://www3.imperial.ac.uk/geometry/seminars/taktic"
  },
  {
    account: '/json/ic/ipgas',
    label: "Imperial College Geometry and Analysis Seminar",
    url: "http://geometry.ma.ic.ac.uk/gaseminar/"
  },
  {
    account: '/json/ic/ipltgs',
    label: "The London Topology and Geometry Seminar",
    url: "http://geometry.ma.ic.ac.uk/seminar/"
  },
  {
    account: '/json/gcal/84rn4klt27550hfpciblhjb71s%40group.calendar.google.com',
    label: "KCL Disordered System Seminar",
    url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/disorderedsys/seminars.aspx"
  },
  {
    account: '/json/gcal/fnmlc1qjb290apdf07h02ut59s%40group.calendar.google.com',
    label: "KCL Theoretical Physics Seminar",
    url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/theorphysics/seminars.aspx"
  },
  {
    account: '/json/ic/sas',
    label: "IC Stochastic Analysis Seminar",
    url: "http://www3.imperial.ac.uk/stochasticanalysisgroup/events"
  },
  {
    account: '/json/ic/apde',
    label: "IC Applied PDEs Seminars",
    url: "http://www3.imperial.ac.uk/ammp/aboutammp/pdesseminars"
  },
  {
    account: '/json/ic/ammp',
    label: "IC Applied Mathematics and Mathematical Physics Seminar",
    url: "http://www3.imperial.ac.uk/ammp/aboutammp/ammpseminar"
  },
  {
    account: '/json/ic/fd',
    label: "IC Fluid dynamics group seminar",
    url: "http://www3.imperial.ac.uk/ammpfluiddynamics/seminars"
  },
  {
    account: '/json/ic/ftmp',
    label: "IC fortnightly seminar on topics in Mathematical Physics",
    url: "http://www3.imperial.ac.uk/mathematicalphysics/events"  
  },
  {
    account: '/json/ic/bms',
    label: "IC biomathematics group's seminar",
    url: "http://www.imperial.ac.uk/biomathematics-group/seminars/"
  }
];

// interface AddThisEvent {
//   refresh():any;
// }
// declare var addthisevent: AddThisEvent;

// Modified when we add new seminars
var lastIndexUpdate = new Date("Fri May 29 2015 19:24:57 GMT+0100 (BST)");
var lastLocalUpdate = JSON.parse(localStorage.getItem('lastUpdate'));

if (!(lastLocalUpdate instanceof Date)) {
  lastLocalUpdate = new Date(lastLocalUpdate);
}

var seminars: ISeminarData[];
var events: { [id: string]: Event; } = {};

if (!localStorage.getItem('seminars') || lastLocalUpdate < lastIndexUpdate) {
  // Add the Id and enable all seminars.
  // Generate the colors in a "rainbow" fashion.
  for (var i = 0; i < seminars_.length; i++) {
    seminars_[i].id = gUUID(),
    seminars_[i].color = genColor(i, seminars_.length);
    seminars_[i].enabled = true;
  }

  seminars = seminars_;
  localStorage.setItem('seminars', JSON.stringify(seminars));
  localStorage.setItem('lastUpdate', JSON.stringify(new Date()));
} else {
  seminars = JSON.parse(localStorage.getItem('seminars'));
}

/*
*
*  Event managment and google calendar scraping
*
*/

// Get basic JSON feed from Google Calendar or our Flask App
// TODO: understand type of the jquery promise.
function getJSON(seminarData: ISeminarData): JQueryPromise<any> {
  var url = apiUrl + seminarData.account;

  return $.getJSON(url).done(function(data) {
    listEvents(data, seminarData);
  });
}

function listEvents(root, seminarData: ISeminarData) {
  var entries = root;
  
  // We elaborates the events (seminars) one by one and throw away anything that
  // is not parsed correctly.
  if (!(seminarData.id in events)) {
      events[seminarData.id] = entries.map(function(evt) { return getEvent(evt, seminarData); }).filter(isNotNull);
  }
  
  $('#calendar').fullCalendar('addEventSource', { events: events[seminarData.id], cid: seminarData.id });
  $('#calendar').fullCalendar('refetchEvents');

  // After populating the calendar, remove the appropriate loading spinner.
  var spinner = "#" + seminarData.id + " .spinner";
  $(spinner).remove();
}

function isNotNull(element): boolean {
  return element != null;
}

// Build the event out of our nice flask-scraped-and-generated json.
// Just a remapping...
function getEvent(entry, seminarData: ISeminarData) {
  return {
    title: entry.title,
    start: new Date(entry.start),
    end: new Date(entry.end),
    where: entry.location,
    content: entry.description + addCalBtn(entry),
    category: seminarData.label,
    categoryUrl: seminarData.url,
    backgroundColor: seminarData.color,
    borderColor: lightenDarkenColor(seminarData.color, -42),
    textColor: lightenDarkenColor(seminarData.color, -112),
    allDay: false
  };
}

// Style and generate the legenda for a given seminar
function legendElement(seminarData: ISeminarData) {
  var item = [
    '<li id="',
    seminarData.id,
    '" style="border-color:',
    lightenDarkenColor(seminarData.color, -42),
    '; background-color:',
    seminarData.color,
    ';">',
    addCheckbox(seminarData),
    '<a style="text-decoration: none; color:',
    ';"><a style="text-decoration: none; color:',
    lightenDarkenColor(seminarData.color, -112),
    ';" href="',
    seminarData.url,
    '" target="_blank">',
    seminarData.label,
    addSpinner(seminarData.enabled),
    '</li>\n'
  ];
  return item.join("");
}

// TODO: See if return type can be made HTMLDivElement | ''
function addSpinner(isEnabled: boolean): string {
  if (isEnabled) {
    return '<div class="spinner"></div>';
  } else {
    return '';
  }
}

// Takes a number num and left-pad it with at most size zeroes
function pad(num, size): string {
  var s = num + "";
  while (s.length < size) s = "0" + s;
  return s;
}

// Takes a date object and returns a string of the form
// MM/DD/YYYY HH:MM
function formatDate(date: Date): string {
  return pad(date.getUTCDate(), 2) +
    '/' + pad(date.getUTCMonth() + 1, 2) + 
    '/' + date.getUTCFullYear() +
    ' ' + pad(date.getUTCHours(), 2) +
    ':' + pad(date.getUTCMinutes(), 2);
}

// Standard format to use https://addthisevent.com/button/ api.
// This may change in the future.
function addCalBtn(seminar): string {
  var sStart = formatDate(new Date(seminar.start));
  var sEnd = formatDate(new Date(seminar.end));
  return '<br/><br/><div title="Add to Calendar" class="addthisevent" data-role="none" rel="external">' +
    'Add to Calendar' +
    '<span class="start">' + sStart + '</span>' +
    '<span class="end">' + sEnd + '</span>' +
    '<span class="timezone">Europe/London</span>' +
    '<span class="title">' + seminar.title + '</span>' +
    '<span class="description">' + seminar.description + '</span>' +
    '<span class="location">' + seminar.location + '</span>' +
    '<span class="date_format">DD/MM/YYYY</span>' +
    '</div>';
}

function addCheckbox(seminarData: ISeminarData): string {
  var checked;
  if (seminarData.enabled) {
    checked = 'checked';
  }
  else {
    checked = '';
  }
  return '<input type="checkbox" ' + checked + ' onclick="seminarClicked(\'' + seminarData.id + '\')"/>';
}

// Generate seminars' legend
function generateLegend(seminars: ISeminarData[]) {
  var legend = ['<h2 id="legendTitle">Colours Legend</h2><ul>'];
  legend = legend.concat(seminars.map(legendElement));
  legend.push('</ul>');
  
  // For some reason I get unpredictable behavior if I don't 
  // first clear the html.
  $('#legend').html("");
  $('#legend').html(legend.join(""));
}

// Gets the data and populates the calendar
function populateCalendar() {
  $('#calendar').fullCalendar('removeEvents');
  seminars.filter(entryEnabled).map(getJSON);
}

function entryEnabled(seminarData: ISeminarData): boolean {
  return seminarData.enabled;
}

$(document).ready(function() {
  generateLegend(seminars);
  populateCalendar();
});

function seminarClicked(cid: string) {
  // This block is hacked up, the "any" allows us to turn off (in some sense)
  // typescript type check of this function.
  // TODO: refactor the code to avoid this hack
  var checkbox = <HTMLInputElement>$("#" + cid + " input")[0];
  for (var i = 0; i < seminars.length; i++) {
    if (seminars[i].id == cid) {
      seminars[i].enabled = !seminars[i].enabled;
      console.log(seminars[i]);
      if (seminars[i].enabled) {
        checkbox.setAttribute("checked", "");
      } else {
        checkbox.removeAttribute("checked");
      }
    }
    if (seminars[i].enabled) {
      var li = $("#" + seminars[i].id)[0];
      li.innerHTML = li.innerHTML + addSpinner(true);
    }
  }
  // I am saving redundant data: the complete series of events. 
  localStorage.setItem('seminars', JSON.stringify(seminars));

  populateCalendar();
}

// TODO: - understand "allDay" events or multiple days ones
