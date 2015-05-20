/// <reference path="typings/tsd.d.ts" />
/*
*
*   Pastel Color Palette generation
*
*/
function rgbToHex(red, green, blue) {
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
function hslToRgb(h, s, l) {
    var r, g, b;
    if (s == 0) {
        r = g = b = l; // achromatic
    }
    else {
        var hue2rgb = function hue2rgb(p, q, t) {
            if (t < 0)
                t += 1;
            if (t > 1)
                t -= 1;
            if (t < 1 / 6)
                return p + (q - p) * 6 * t;
            if (t < 1 / 2)
                return q;
            if (t < 2 / 3)
                return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        };
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
function genColor(idx, l) {
    var rgb = hslToRgb(idx * (1.2) / (2 * l) + 0.02, 0.65, 0.83);
    return rgbToHex.apply(this, rgb);
}
// Takes a HEX coluor and add the provided amount to each component.
// Use negative numbers to darken (do not exaggerate).
// credits: http://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
function lightenDarkenColor(col, amt) {
    // we use slice to get rid of the # in front of the colour
    var num = parseInt(col.slice(1), 16);
    var r = (num >> 16) + amt;
    var b = ((num >> 8) & 0x00FF) + amt;
    var g = (num & 0x0000FF) + amt;
    return rgbToHex(r, g, b);
}
function darken(col) {
    return lightenDarkenColor(col, -42);
}
/*
*
*   Seminars data configuration, types and helpers
*
*/
// RFC4122 version 4 compliant UUID generator.
function gUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
// TODO: These will be later loaded from a separate JSON file, 
// for the moment we manage them by hand here.
var apiUrl = "//mathcal-mseri.rhcloud.com";
var seminars_ = [{
        account: '/json/las',
        label: "London Analysis and Probability Seminar",
        url: "http://www.london-analysis-seminar.org.uk/",
        parser: "flask"
    },
    {
        account: 'imperial.pure.analysis%40gmail.com',
        label: "Imperial College Analysis Seminar",
        url: "http://www.imperial.ac.uk/a-z-research/mathematical-analysis/pure-analysis-and-pdes/activities/",
        parser: "gCal"
    },
    {
        account: 'gkij4q9m1249c2osijddav6dig%40group.calendar.google.com',
        label: "KCL Analysis Seminar",
        url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/analysis/events/seminars.aspx",
        parser: "gCal"
    },
    {
        account: '/json/ic/ip',
        label: "Imperial Probability Centre",
        url: "http://wwwf.imperial.ac.uk/~amijatov/IP/index.php",
        parser: "flask"
    },
    {
        account: '/json/nts',
        label: "Number Theory Seminar",
        url: "http://www.homepages.ucl.ac.uk/~ucahsze/seminars.html",
        parser: "flask"
    },
    {
        account: 'giu2ael3iq4sd9ucqa2uur7048%40group.calendar.google.com',
        label: "KCL/UCL Geometry Seminar",
        url: "http://www.ucl.ac.uk/geometry/seminars.htm",
        parser: "gCal"
    },
    {
        account: 'magicseminar%40googlemail.com',
        label: "MAGIC Seminar",
        url: "http://coates.ma.ic.ac.uk/magic/",
        parser: "gCal"
    },
    {
        account: '/json/ic/taktic',
        label: "TAKTIC: Topology and Knot Theory at Imperial College",
        url: "http://www3.imperial.ac.uk/geometry/seminars/taktic",
        parser: "flask"
    },
    {
        account: '/json/ic/ipgas',
        label: "Imperial College Geometry and Analysis Seminar",
        url: "http://geometry.ma.ic.ac.uk/gaseminar/",
        parser: "flask"
    },
    {
        account: '/json/ic/ipltgs',
        label: "The London Topology and Geometry Seminar",
        url: "http://geometry.ma.ic.ac.uk/seminar/",
        parser: "flask"
    },
    {
        account: '84rn4klt27550hfpciblhjb71s%40group.calendar.google.com',
        label: "KCL Disordered System Seminar",
        url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/disorderedsys/seminars.aspx",
        parser: "gCal"
    },
    {
        account: 'fnmlc1qjb290apdf07h02ut59s%40group.calendar.google.com',
        label: "KCL Theoretical Physics Seminar",
        url: "http://www.kcl.ac.uk/nms/depts/mathematics/research/theorphysics/seminars.aspx",
        parser: "gCal"
    },
    {
        account: '/json/ic/sas',
        label: "IC Stochastic Analysis Seminar",
        url: "http://www3.imperial.ac.uk/stochasticanalysisgroup/events",
        parser: "flask"
    },
    {
        account: '/json/ic/apde',
        label: "IC Applied PDEs Seminars",
        url: "http://www3.imperial.ac.uk/ammp/aboutammp/pdesseminars",
        parser: "flask"
    },
    {
        account: '/json/ic/ammp',
        label: "IC Applied Mathematics and Mathematical Physics Seminar",
        url: "http://www3.imperial.ac.uk/ammp/aboutammp/ammpseminar",
        parser: "flask"
    },
    {
        account: '/json/ic/fd',
        label: "IC Fluid dynamics group seminar",
        url: "http://www3.imperial.ac.uk/ammpfluiddynamics/seminars",
        parser: "flask"
    },
    {
        account: '/json/ic/ftmp',
        label: "IC fortnightly seminar on topics in Mathematical Physics",
        url: "http://www3.imperial.ac.uk/mathematicalphysics/events",
        parser: "flask"
    }
];
// Modified when we add new seminars
var lastIndexUpdate = new Date("Wed May 19 2015 00:41:57 GMT+0100 (BST)");
var lastLocalUpdate = JSON.parse(localStorage.getItem('lastUpdate'));
var seminars;
var events = {};
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
}
else {
    seminars = JSON.parse(localStorage.getItem('seminars'));
}
/*
*
*  Event managment and google calendar scraping
*
*/
// Get basic JSON feed from Google Calendar or our Flask App
// TODO: understand type of the jquery promise.
function getJSON(seminarData) {
    var url;
    if (seminarData.parser == "gCal") {
        url = 'https://www.google.com/calendar/feeds/' + seminarData.account + '/public/basic?alt=json&hl=en';
    }
    else {
        url = apiUrl + seminarData.account;
    }
    return $.getJSON(url).done(function (data) {
        listEvents(data, seminarData);
    });
}
function listEvents(root, seminarData) {
    var entries;
    // Google calendar has a slightly different JSON structure;
    // we need to deal with it separately
    if (seminarData.parser == "gCal") {
        var feed = root.feed;
        entries = feed.entry || [];
    }
    else {
        entries = root;
    }
    // We elaborates the events (seminars) one by one and throw away anything that
    // is not parsed correctly.
    if (!(seminarData.id in events)) {
        events[seminarData.id] = entries.map(getEventFrom(seminarData)).filter(isNotNull);
    }
    $('#calendar').fullCalendar('addEventSource', { events: events[seminarData.id], cid: seminarData.id });
    $('#calendar').fullCalendar('refetchEvents');
    // After populating the calendar, remove the appropriate loading spinner.
    var spinner = "#" + seminarData.id + " .spinner";
    $(spinner).remove();
}
function isNotNull(element) {
    return element != null;
}
// Generate getEvent function to elaborate the entries from the
// JSON feeds.
function getEventFrom(seminarData) {
    return function getEvent(entry) {
        if (seminarData.parser == "gCal") {
            return getGCalEvent(entry, seminarData);
        }
        else {
            return getFlaskEvent(entry, seminarData);
        }
    };
}
// Build the events out of Google calendar's feed entries.
// We use horrible hacked regex parsing of the content to extract and 
// re-elaborate the data. Trust me, it's not nice to read!
function getGCalEvent(entry, seminarData) {
    // This is the easy bit, just get title and content.
    var title = (entry.title.type == 'html') ? entry.title.$t : encodeURI(entry.title.$t);
    // Workaround for duplicate London Analysis Seminar 
    // from Imperial Analysis calendar
    if (title.slice(0, 4) == "LANS") {
        return null;
    }
    if (title.indexOf("London Analysis and Probability Seminar") > -1) {
        return null;
    }
    var content = (entry.content.type == 'html') ? entry.content.$t : encodeURI(entry.content.$t);
    // Get When and Where from the formatted content in the google calendar string
    // Takes a string of the form
    //
    // When: Thu Feb 19, 2015 3pm to 4pm \nGMT\u003cbr /\u003e\n\n\u003cbr /\u003eWhere: room S423\n\u003cbr /\u003eEvent Status: confirmed\n\u003cbr /\u003eEvent Description: some description
    // 
    // strips it and then scrapes from it date, time, location and description.
    var strippedContent = content.replace(/(<br \/>|\n)/g, '§');
    var wAndWRegex = /When: (\w{3} \w{3} \d+, \d{4} \d+:?\d*[ap]m) to (.*\d+:?\d*[ap]m).*Where: ([^§]*)§+.*/;
    var whenAndWhere_ = wAndWRegex.exec(strippedContent);
    var descRegex = /.*Event Description: (.*)/;
    var description_ = descRegex.exec(strippedContent);
    // whenAndWhere infos are essential. 
    // If something went wrong with them we are not going to process the event.
    if (whenAndWhere_) {
        // Get rid of strippedContent, the original string, 
        // contained at the beginning of the array.
        var whenAndWhere = whenAndWhere_.splice(1);
        // Fix start and stop datetime format:
        // get (\d\d?)([ap]m) and make into $1:00 $2
        var start = new Date(whenAndWhere[0].replace(/([ap]m)/, " $1").replace(/ (\d\d?) /, " $1:00 "));
        // Add day in front of stop string and fix the time.
        // FIXME: I am assuming start/stop in the same day.
        var stop = new Date(whenAndWhere[0].replace(/\d\d?:?\d?\d?\s?[ap]m/, whenAndWhere[1]).replace(/([ap]m)/, " $1").replace(/ (\d\d?) /, " $1:00 "));
        var where = whenAndWhere[2];
        var description = "";
        if (description_) {
            description = description_[1].replace(/§/g, '<br />');
        }
        return {
            title: title,
            start: start,
            end: stop,
            where: where,
            content: description,
            category: seminarData.label,
            categoryUrl: seminarData.url,
            backgroundColor: seminarData.color,
            borderColor: lightenDarkenColor(seminarData.color, -42),
            textColor: lightenDarkenColor(seminarData.color, -112),
            allDay: false
        };
    }
    return null;
}
// Build the event out of our nice flask-scraped-and-generated json.
// Just a remapping...
function getFlaskEvent(entry, seminarData) {
    return {
        title: entry.title,
        start: new Date(entry.start),
        end: new Date(entry.end),
        where: entry.location,
        content: entry.description,
        category: seminarData.label,
        categoryUrl: seminarData.url,
        backgroundColor: seminarData.color,
        borderColor: lightenDarkenColor(seminarData.color, -42),
        textColor: lightenDarkenColor(seminarData.color, -112),
        allDay: false
    };
}
// Style and generate the legenda for a given seminar
function legendElement(seminarData) {
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
function addSpinner(isEnabled) {
    if (isEnabled) {
        return '<div class="spinner"></div>';
    }
    else {
        return '';
    }
}
function addCheckbox(seminarData) {
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
function generateLegend(seminars) {
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
function entryEnabled(seminarData) {
    return seminarData.enabled;
}
$(document).ready(function () {
    generateLegend(seminars);
    populateCalendar();
});
function seminarClicked(cid) {
    // This block is hacked up, the "any" allows us to turn off (in some sense)
    // typescript type check of this function.
    // TODO: refactor the code to avoid this hack
    var checkbox = $("#" + cid + " input")[0];
    for (var i = 0; i < seminars.length; i++) {
        if (seminars[i].id == cid) {
            seminars[i].enabled = !seminars[i].enabled;
            console.log(seminars[i]);
            if (seminars[i].enabled) {
                checkbox.setAttribute("checked", "");
            }
            else {
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
// TODO: - remove gmail scraper and add it to the backend
//       - understand "allDay" events or multiple days ones
