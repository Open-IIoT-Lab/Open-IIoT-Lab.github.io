(function () {
    'use strict';
    var form = document.getElementById('publication-filters');
    if (!form) return;
    var search = document.getElementById('publication-search');
    var year = document.getElementById('publication-year');
    var type = document.getElementById('publication-type');
    var topic = document.getElementById('publication-topic');
    var code = document.getElementById('publication-code');
    var count = document.getElementById('publication-count');
    var empty = document.getElementById('publication-empty');
    var records = Array.from(document.querySelectorAll('#publication-archive .classic-publication')).map(function (element) {
        return {element: element, text: normalize(element.textContent), year: element.dataset.year, kind: element.dataset.kind, topics: element.dataset.topics.split(' '), code: element.dataset.code === 'true'};
    });
    var sections = Array.from(document.querySelectorAll('.classic-archive-year'));
    var yearLinks = Array.from(document.querySelectorAll('#navbar-year a[data-year]'));
    function normalize(text) {
        return text.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[\u2010-\u2015]/g, '-');
    }
    function update(writeURL) {
        var terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
        var visible = 0;
        records.forEach(function (record) {
            var match = (!year.value || record.year === year.value) && (!type.value || record.kind === type.value) && (!topic.value || record.topics.indexOf(topic.value) !== -1) && (!code.checked || record.code) && terms.every(function (term) { return record.text.indexOf(term) !== -1; });
            record.element.hidden = !match;
            if (match) visible++;
        });
        sections.forEach(function (section) {
            var n = section.querySelectorAll('.classic-publication:not([hidden])').length;
            section.hidden = n === 0;
            section.querySelector('.classic-year-count').textContent = '(' + n + ')';
            yearLinks.forEach(function (link) { if (link.dataset.year === section.dataset.year) link.hidden = n === 0; });
        });
        count.textContent = visible === records.length ? records.length + ' publications' : visible + ' of ' + records.length + ' publications';
        empty.hidden = visible !== 0;
        if (writeURL) {
            var url = new URL(window.location.href);
            var values = {q: search.value.trim(), year: year.value, type: type.value, topic: topic.value, code: code.checked ? '1' : ''};
            Object.keys(values).forEach(function (key) { if (values[key]) url.searchParams.set(key, values[key]); else url.searchParams.delete(key); });
            window.history.replaceState(null, '', url.pathname + url.search + url.hash);
        }
        document.dispatchEvent(new Event('publications:filtered'));
    }
    function revealAnchor() {
        var target;
        try { target = document.getElementById(decodeURIComponent(window.location.hash.slice(1))); } catch (error) { return; }
        if (target && target.closest('.classic-publication[hidden]')) {
            form.reset();
            update(true);
            target.scrollIntoView();
        }
    }
    var params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    year.value = params.get('year') || '';
    type.value = params.get('type') || '';
    var requestedTopic = params.get('topic') || '';
    topic.value = {wireless: 'networks', sensing: 'intelligence'}[requestedTopic] || requestedTopic;
    code.checked = params.get('code') === '1';
    form.hidden = false;
    form.addEventListener('input', function () { update(true); });
    form.addEventListener('change', function () { update(true); });
    form.addEventListener('submit', function (event) { event.preventDefault(); update(true); });
    form.addEventListener('reset', function () { window.setTimeout(function () { update(true); }, 0); });
    window.addEventListener('hashchange', revealAnchor);
    update(false);
    revealAnchor();
}());
