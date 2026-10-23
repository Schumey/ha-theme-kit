/*
 * My Theme – loads mytheme.css (font, cursor, scrollbars)
 * Version: 0.1.0
 *
 * Registered as a frontend script by the integration; the stylesheet lies next to it.
 */
const link = document.createElement("link");
link.rel = "stylesheet";
link.href = new URL("mytheme.css", import.meta.url).href;
document.head.appendChild(link);
