(function () {
    var navigation = document.querySelector('.classic-year-navigation');
    if (!navigation) return;
    var links = Array.from(navigation.querySelectorAll('a[href^="#"]'));
    var sections = links.map(function (link) { return document.getElementById(link.hash.slice(1)); });
    function update() {
        var current = sections.find(function (section) { return section && !section.closest('[hidden]'); });
        sections.forEach(function (section) {
            if (section && !section.closest('[hidden]') && section.getBoundingClientRect().top <= 24) current = section;
        });
        links.forEach(function (link) {
            if (current && link.hash === '#' + current.id) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
        });
    }
    var pending = false;
    window.addEventListener('scroll', function () {
        if (pending) return;
        pending = true;
        requestAnimationFrame(function () { update(); pending = false; });
    }, {passive: true});
    window.addEventListener('hashchange', update);
    document.addEventListener('publications:filtered', update);
    if (document.fonts) document.fonts.ready.then(update);
    update();
})();
