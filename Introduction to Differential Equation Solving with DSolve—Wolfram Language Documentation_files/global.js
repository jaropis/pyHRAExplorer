/* REFERENCE SITE GLOBAL FUNCTIONALITIES

   developer:   suef
   requires:    jQuery
   ========================================================================== */

$(document).ready(function(){
/* ==========================================================================
   Toggles
   ========================================================================== */
    $('.toggle').click(function(){
        if($(this).parents('section').attr('id') !== "Examples") {
            $(this).toggleClass('open');
        }
    });
    $('#Examples').on('click', '.toggle', function(){
        var clicked = $(this);
        clicked.toggleClass('open');
        if(clicked.hasClass('load')) {
            $('.load').each(function(i){
                $(this).attr('data-content', i+1);
            });
            var index = clicked.attr('data-content');
            var fileurl = 'Files/'+baselang+'/'+baselang.split('.')[0].toLowerCase()+index+'.html';
            $.ajax({
                type: "GET",
                async: false,
                url: fileurl,
                dataType: "html",
                success: function(data) {
                    clicked.next('.hideable').html(data);
                }
            });
        }
    });
    $('.open-all').click(function(){
        $('.open-all').removeClass('on');
        $('.close-all').addClass('on');
        $('#Examples .toggle').addClass('open');
        if($('#Examples .toggle').hasClass('load')) {
            $('.load').each(function(i){
                load = $(this);
                load.attr('data-content', i+1);
                index = load.attr('data-content');
                fileurl = 'Files/'+baselang+'/'+baselang.split('.')[0].toLowerCase()+index+'.html';
                $.ajax({
                    type: "GET",
                    async: false,
                    url: fileurl,
                    dataType: "html",
                    success: function(data) {
                        load.next('.hideable').html(data);
                    }
                });
            });
        }
    });
    $('.close-all').click(function(){
        $('.open-all').addClass('on');
        $('.close-all').removeClass('on');
        $('#Examples .hideable .toggle').removeClass('open');
    });
    $('.NotesThumbnails').click(function(){
        $(this).siblings('h1').toggleClass('open');
    });
    $('.feedback').click(function(){
        $('#feedbackForm').toggleClass('opened');
    });
    $('#submit').on("click", function(e) {
        e.preventDefault();
        var feedbackval = $('#feedbackMessage').val();

        if(feedbackval === null || feedbackval === '')
        {
           $('#feedbackMessageTable').addClass('errorHighlight');
        }
        else {
            $('div#thank_you').removeClass('hide');
            $('table#formTable').addClass('hide');
            $('#feedbackMessageTable').removeClass('errorHighlight');
            $.post("/language-assets/inc/feedback.cgi", {
                   feedback: $('#feedbackMessage').val(),
                   name: $('input#name').val(),
                   email: $('input#email').val(),
                   url: document.URL
            } );
        }
    });

    if($('.toggle').length) {
        $('.toggle + .hideable').find('> :last-child').addClass('last');
    }

/* ==========================================================================
   Notes tables styling based on column width
   ========================================================================== */
    $('.NotesTable').each(function() {
        if ($(this).find('col').length == 4) {
            $(this).addClass('three-col');
        } else if ($(this).find('col').length == 3) {
            $(this).addClass('two-col');
        }
    });

/* ==========================================================================
   Sticky Alphabet listing
   ========================================================================== */
    if ($('.AlphabetListingJumpTo').length) {
        var left = document.getElementsByClassName('AlphabetListingJumpTo')[0];
        var stop = (left.offsetTop - 60);
        var lastScroll = 0;
        window.onscroll = function(e) {
            var st = $(this).scrollTop();
            var scrollTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
            if (scrollTop >= stop && st < lastScroll) {
                left.className = 'AlphabetListingJumpTo sticky';
            } else {
                left.className = 'AlphabetListingJumpTo';
            }
            lastScroll = st;
        }
        $('.AlphabetListingJumpTo a').click(function() {
            var id = $(this).prop('href').split("#")[1];
            $('html,body').animate({
                scrollTop: $('#' + id).offset().top - 65 //offset height of header here too.
            }, 1000);
        });
    }

/* ==========================================================================
   Dropdowns
   ========================================================================== */
    $("ul.dropdown > li > a").on('click mouseover', function() {
        $("ul.dropdown > li").not($(this).parents("li")).removeClass("hover");
        $(this).parents("li").toggleClass("hover");
        var elm = $(this).parents("li").find('.sub_menu');
        var off = elm.position();
        var l = off.left;
        var w = elm.outerWidth();
        var docW = $(".main").outerWidth();
        var isEntirelyVisible = (l + w <= docW);

        if (!isEntirelyVisible) {
            if (w > 425 && docW <= 430) {
                $(this).parents("li").addClass("shrink");
            }
            $(this).parents("li").addClass('edge');
        } else {
            $(this).parents("li").removeClass('edge');
        }
        var mainWrapperHeight = $('.main').height(); // height of main wrapper
        var dropdownHeight = $('li.hover ul').height() + 291; // height of selected dropdown
        if (dropdownHeight > mainWrapperHeight && $(this).parents("li").hasClass("hover")) {
            $('.main').height(dropdownHeight);
        } else {
            $('.main').css('height', 'auto');
        }
    });
    $('.dropdown > li').on('mouseleave', function(){
        $(this).removeClass("hover").removeClass("edge");
        $('.main').css('height', 'auto');
    });

/* ==========================================================================
   Highlight
   ========================================================================== */
    $('.highlight-link').click(function() {
        $('highlighting').not(this).toggleClass('highlighting');
        $(this).toggleClass('highlighting');
        $('.modified-text').toggleClass('highlighting');
        $('#DetailsAndOptions h1').toggleClass('highlighting');
    });

/* ==========================================================================
   Search
   ========================================================================== */
    $("#ref-search-form").submit(function() {
        $.ajax({
            type: "GET",
            traditional: true,
            url: "/search-api/search.json",
            dataType: "json",
            data: {
                query: $("#query").val(),
                limit: 3,
                disableSpelling: true,
                collection: ["documentation10"],
                fields: "uri,title"
            },

            success: function(data) {
                if(data.adResult) {
                    if(data.adResult.fields.title[0] == $("#query").val()) {
                        location.href = "/language/" + data.adResult.fields.uri[0] + ".html?q=" + encodeURIComponent($("#query").val());
                    } else {
                            location.href = "/search/?q="+ encodeURIComponent($("#query").val());
                    }
                } else {
                    location.href = "/search/?q="+ encodeURIComponent($("#query").val());
                }
            }

        });
        return false;
    });
    if(window.location.search.length) {
        if(window.location.search.indexOf('?q=') > -1) {
            $('.search #query').prop('value', decodeURIComponent(window.location.search.split('?q=')[1]));
            $('.search #query').addClass('term-found');
        }
    }
    $('.search #query').on('keypress', function(){
        $('.search #query').addClass('term-found');
    });
/* ==========================================================================
   Tooltips in top icons
   ========================================================================== */
    if($('.media')) {
        $('.media').on('mouseenter', function(){
            $('.media').removeClass('hover');
            $(this).addClass('hover');
        });
        $('.media').on('click', function(){
            $(this).toggleClass('hover');
        });
        $('.tooltip, .media-icons').on('mouseleave', function(){
            $('.media').removeClass('hover');
        });
    }
});
$(window).on('load resize', function() {
/* ==========================================================================
   Ins and outs collapsing to numbers with half brackets
   ========================================================================== */
    $('.lab').each(function(){
        if($(this).text().indexOf('[') > -1) {
            var number = $(this).text().split('[')[1].split(']')[0];
            if($(window).outerWidth() < 600) {
                if($(this).parents('.InCell').find('.number').length < 1) {
                    $(this).parents('.InCell tr').prepend('<td class="number">'+number+'</td>');
                }
                if($(this).parents('.OCell').find('.number').length < 1) {
                    $(this).parents('.OCell tr').prepend('<td class="number">'+number+'</td>');
                }
            }
        }
    });
/* ==========================================================================
   Images swap
   ========================================================================== */
    $('.InCell img').each(function() {
        if($(this).is('[data-src]')) {
            if ($(window).width() < 600) {
                var src = $(this).attr('data-src');
                var extension = src.split('.')[2];
                var w = $(this).attr('data-small').split(' ')[0];
                var h = $(this).attr('data-small').split(' ')[1];
                if (src.indexOf('_405') < 0) {
                    $(this).prop('src', src.replace('.'+extension, '_405.'+extension));
                    $(this).prop('width', w);
                    $(this).prop('height', h);
                }
            } else {
                var src = $(this).attr('data-src');
                var w = $(this).attr('data-big').split(' ')[0];
                var h = $(this).attr('data-big').split(' ')[1];
                $(this).prop('src', src);
                $(this).prop('width', w);
                $(this).prop('height', h);
            }
        }
    });
/* ==========================================================================
   Search swap
   ========================================================================== */
    if($(window).width() < 600) {
        $('.no-bfc').prop('action', '/search/');
        $('#_search-input').prop('name', 'q');
        $('input[name="source"').remove();
    }
});

/* ==========================================================================
   Back to top link
   ========================================================================== */
$(window).on('load resize scroll', function() {
    if($('.feedback').length) {
        var offset = 250;
        var duration = 100;
        var main_scroll_height = $('.feedback').offset().top;
        var topLinkPos = $('.toplink').offset().top;
        var height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        if ($(this).scrollTop() > offset) {
            $('.toplink').fadeIn(duration);
            if (topLinkPos >= main_scroll_height) {
                $('.toplink').addClass('above-footer');
            }
            if (topLinkPos > height + $(document).scrollTop()) {
                $('.toplink').removeClass('above-footer');
            }
        } else {
            $('.toplink').fadeOut(duration);
        }
    }
});
$(document).ready(function(){
    $('.toplink').click(function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: 0
        }, 100);
        return false;
    });
});

$(window).on('ready load hashchange', function() {
/* ==========================================================================
   Open anchor location even on closed content
   ========================================================================== */
   if(window.location.hash) {
        var jumpLocation = window.location.hash.replace('#','');
        if(isNaN(jumpLocation) == false) {
            var foundLocation = false;
            $('#Examples a').each(function(){
                if($(this).prop('name') == jumpLocation) {
                    foundLocation = true;
                    $(this).parents('.hideable').prev('.toggle').addClass('open');
                }
            });
            if(foundLocation == false) {
                $('.load').each(function(i){
                    var loadThis = $(this);
                    $(this).attr('data-content', i+1);
                    var index = loadThis.attr('data-content');
                    var fileurl = 'Files/'+baselang+'/'+baselang.split('.')[0].toLowerCase()+index+'.html';
                    $.ajax({
                        type: "GET",
                        async: false,
                        url: fileurl,
                        dataType: "html",
                        success: function(data) {
                            if(data.indexOf(jumpLocation) > -1) {
                                loadThis.next('.hideable').html(data);
                                loadThis.addClass('open');
                            }
                        }
                    });
                });
            }
        }
    }
});

/* ==========================================================================
   Flash manipulates
   ========================================================================== */
function swap(obj, theWidth, theHeight, fileName, divId) {
    var flash1 = '<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=7,0,0,0" width="' + theWidth + '" height="' + theHeight + '" id="benefits" align="middle"><param name="allowScriptAccess" value="sameDomain" /><param name="movie" value="' + fileName + '" /><param name="loop" value="false" /><param name="menu" value="false" /><param name="quality" value="high" /><param name="bgcolor" value="#ffffff" /><embed src="' + fileName + '" loop="false" menu="false" quality="high" bgcolor="#ffffff" width="' + theWidth + '" height="' + theHeight + '" name="benefits" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" /></object>';

    document.getElementById(divId).innerHTML = flash1;
}