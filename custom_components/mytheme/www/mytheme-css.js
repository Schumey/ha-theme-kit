/*
 * My Theme – loads mytheme.css (font, cursor, scrollbars)
 * Version: 0.5.0
 *
 * Registered as a frontend script by the integration; the stylesheet lies next to it.
 */
const link = document.createElement("link");
link.rel = "stylesheet";
// Pass on ?v=<version> from this script, or browsers keep the old stylesheet after an update
const url = new URL("mytheme.css", import.meta.url);
url.search = new URL(import.meta.url).search;
link.href = url.href;
document.head.appendChild(link);
