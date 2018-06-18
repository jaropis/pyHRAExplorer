$(document).ready(function() {
    /* Mouse events
    ============================================================*/
    var delay = 1500, setTimeoutConst;
    if($(window).outerWidth() < 601) {
        delay = 0;
    }
    $(window).resize(function(){
        if($(window).outerWidth() < 601) {
            delay = 0;
        } else {
            delay = 1500;
        }
    });
    $(document).on('mouseenter', '.InCell', function() {
        var inCell = $(this);
        load_copy_text(inCell);
        inCell.find('.IFL').after('<div class="clipboard"></div>');
        setTimeoutConst = setTimeout(function(){
            inCell.find('.clipboard').after('<div class="tooltip">Copy to clipboard.</div>');
            inCell.addClass('hover');
            var visible = $('.InCell .tooltip').isOnScreen(0.5, 0.5);
            if(!visible) {
                $('.InCell .tooltip').addClass('bottom');
            } else {
                $('.InCell .tooltip').removeClass('bottom');
            }
        }, delay);
    });
    $(document).on('mouseleave', '.InCell', function() {
        clearTimeout(setTimeoutConst);
        $('.InCell .tooltip, .InCell .clipboard').remove();
        $(this).removeClass('hover');
    });
    $(document).on('mouseup', '.InCell', function(e){
        var clicked_element = $(this);
        select_copy_text(clicked_element.find('.text').prop('id'));

        // check support for copy
        if (document.queryCommandSupported('copy')) {
            var successful = document.execCommand('copy');
            var text = '';
            var msg = successful ? text = 'Copied!' : text = 'Unable to copy.';
            $('.InCell .tooltip').text(text);
            clicked_element.find('.clipboard').addClass('copied');
            if($('.InCell .tooltip').length < 1) {
                clicked_element.find('.InCell .clipboard').after('<div class="tooltip">Copied!</div>');
            }
        }
        else {
            $('.IFL').removeClass('show');
            $(this).find('.IFL').addClass('show');
            $('.InCell .tooltip').remove();
            $(document).on('mouseup', '.close', function(e){
                e.stopPropagation();
                $(this).parents('.IFL').removeClass('show');
            });
        }
    });
    /* touch events
    =====================================================*/
    $(document).on('touchstart', function() {
        $('.InCell .clipboard, .InCell .tooltip').remove();
    });
    $(document).on('touchstart', '.InCell', function() {
        window.oncontextmenu = function (event) {
            event.preventDefault();
            event.stopPropagation();
            return false;
        };
        load_copy_text($(this));
        $('.InCell .clipboard, .InCell .tooltip').remove();
        $(this).addClass('hover');
        $(this).find('.IFL').after('<div class="clipboard"></div><div class="tooltip">Copy to clipboard</div>');
        tapFlag = true;
    });
    $(document).on('touchend', '.InCell', function(e) {
        if (tapFlag !== false) {

            select_copy_text($(this).find('.text').prop('id'));
            $('.InCell .clipboard, .InCell .tooltip').remove();
            // check support for copy
            if (document.queryCommandSupported('copy')) {
                var successful = document.execCommand('copy');
                $(this).find('.IFL').after('<div class="clipboard"></div><div class="tooltip">Copied!</div>');
                $(this).find('.clipboard').addClass('copied');
            }
            else {
                $(this).find('.IFL').addClass('show');
                $(document).on('touch', '.close', function(e){
                    e.stopPropagation();
                    $(this).parents('.IFL').removeClass('show');
                });
            }
            e.preventDefault();
            touchFlag = false;
        }
    });
    $(document).on('touchmove', function(e) {
        $('.InCell .clipboard, .InCell .tooltip').remove();
        tapFlag = false;
    });
    var select_copy_text = function(el) {
        var doc = window.document, sel, range;
        var el = document.getElementById(el);
        if (window.getSelection && doc.createRange) {
            sel = window.getSelection();
            range = doc.createRange();
            range.selectNodeContents(el);
            sel.removeAllRanges();
            sel.addRange(range);
        } else if (doc.body.createTextRange) {
            range = doc.body.createTextRange();
            range.moveToElementText(el);
            range.select();
        }
    };
    var load_copy_text = function(clicked_element) {
        var id_out = clicked_element.find('.IFL').prop('id');
        var file = 'Files/'+ baselang + '/' + id_out.replace('_out','') +'.txt';
        if(clicked_element.find('.IFL').text() == '') { // if file hasn't loaded already
            $.ajax({
                url: file,
                dataType: "text",
                success: function(data) {
                    var text = data.replace(/(\r|\n)+/g, '\n');
                    var innertxt = text.match(/<pre(?:.*?)>(.|\n)+<\/pre>/)[0].replace(/(<([^>]+)>)/ig,"");
                    $('#'+id_out).html('<span class="close">&#x2715;</span><pre id="'+id_out+'_text" class="text">'+innertxt+'</pre>');
                }
            });
        }
    };
});
$.fn.isOnScreen = function(){
    var element = this.get(0);
    var bounds = element.getBoundingClientRect();
    return bounds.top < window.innerHeight && bounds.bottom > 0;
}