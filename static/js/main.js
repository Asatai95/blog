
// ----------------------------- 共通コード--------------------------------------
// ログイン画面、ラベル横のやつ消す
$(function(){
    $("div label").each(function(){

        $(this).text().replace(":", "");
    });
});

// カテゴリー、タグアイコンを選択時のイベント
$(function(){
    $(".card .row .col.main_box .card-body .card-text.topic span a").each(function(){
        $(this).parents("span").on("mouseover mouseout", function(e){
            if (e.type == "mouseover") {
                $(this).css("box-shadow", "0 0 3px #222");
            }
            if (e.type == "mouseout") {
                $(this).css("box-shadow", "0 0 0");
            }
        });
    });
    $(".card .row .col-md-8 .card-body .card-text.topic span a").each(function(){
        $(this).parents("span").on("mouseover mouseout", function(e){
            if (e.type == "mouseover") {
                $(this).css("box-shadow", "0 0 3px #222");
            }
            if (e.type == "mouseout") {
                $(this).css("box-shadow", "0 0 0");
            }
        });
    });
});

$(function(){
    $(window).on("scroll", function(){
        var scrollPosition = $(window).height() + $(window).scrollTop();
        var scrollHeight = $(document).height();
        if (scrollHeight - scrollPosition == 0) {
            $("footer").fadeIn(800);
        } else {
            $("footer").hide();
        }
    });
    var tmp_list = [];
    var random = Math.floor( Math.random() * (6 - 0) ) + 0;
    tmp_list.push(random)
    var random_max = Math.floor( Math.random() * (10 - 6) ) + 6;
    tmp_list.push(random_max)
    var tmp_count_list = [];
    $(".article_text_link").removeClass("active");
    $(".article_text_link").each(function(index){
        tmp_count_list.push(index)
        if (index == tmp_list[0] || index == tmp_list[1]){
            $(this).addClass("active");
        }
    });
    if (tmp_count_list.length > 4) {
        $(".bottom_article_tile_link").css("height", "750px");
    }

    $(".article_text_link").each(function(){
        $(this).on("click", function(){
            var link = $(this).find("a").attr("href");
            window.location.href = link;
        });
    });
});

// ページトップスクロールアイコン
$(function(){
    $('.page_top').hide();
    $(window).scroll(function () {
        if($(window).scrollTop() > 0) {
            $('.page_top').slideDown(300);
        } else {
            $('.page_top').slideUp(300);
        }
    });
    $('.page_top').click(function () {
      $("html,body").animate({scrollTop:0}, 1200, 'swing');
    });
    $(".page_top").mouseover(function(){
      $(this).find("img").css("transform", "scale(1.1)");
    });
    $(".page_top").mouseout(function(){
      $(this).find("img").css("transform", "");
    });
});
// --------------------------------------------------------------------------------

// 投稿作成(管理者画面)
// 投稿ブロックの追加
$(function(){
    $(".select_box").each(function(){
        $(this).find("select").change(function(){
            var value = $(this).val();
            $(this).parents(".select_box").next("p").find("input").val(value);
        });
    });
    $(".more_information p a").on("click", function(e){
        e.preventDefault();
    });
    $(".main_article_info_block").each(function(){
        var content = $(this).find(".article_info.contents").html();
        $(".more_information p a").on("click", function(e){
            e.preventDefault();
            var index_list = [];
            $(".main_article_info_block").find(".article_info.contents").each(function(index){
                index_list.push(index);
            });
            $(".main_article_info_block").find(".article_info.contents").each(function(index){
                if (index == index_list.length - 1) {
                    $(this).after(
                        "<div class='article_info contents'>"+content+"</div>"
                    );
                }
            });
            var count_box = [];
            $(".content_block").each(function(index){
                count_box.push(index);
            });
            $(".content_block").each(function(index){
                if (count_box[count_box.length - 1] == index) {
                    $(this).find("p input").val(index + 1);
                }
            });
        });
    });

    $(document).ready(function() {

        $(".cloudinary-fileupload").cloudinary_fileupload({
          replaceFileInput: false,
          autoUpload: false,
          maxFileSize: 10000000,
          loadImageMaxFileSize: 10000000,
          acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
        })
        .bind('fileuploadadd', function(e, data) {
          console.log(data)
          var file = data.files[0].name;
          var array = [".gif", ".png", ".jpg", ".jpeg"];
          var count = 0;
          for (var i = 0; i < array.length; i++) {
            if (file.indexOf(array[i]) > -1) {count += 1}
          }

          upload = data.submit();
          if (count === 0){
            upload.abort();
            upload = null;
          }
        })
        .bind("fileuploadfail", function(e, data){
          $(".progress_main_box").fadeOut();
          $(this).parents(".image_block").find(".select_box .error_message").show();
        })
        .bind('cloudinaryprogressall', function(e, data) {
          $('.progress_bar .bar').css('width', Math.round((data.loaded * 100.0) / data.total) + '%');
        })
        .bind('cloudinarydone', function(e, data) {
          console.log(data.result.public_id)
          var img_link = "https://res.cloudinary.com/db5nsevmi/" + data.result.public_id;
          $(this).parents(".select_box").find(".image_pre").append(
              '<img src="'+img_link+'" alt="">'
          )
        });
    });

    $(".add_link").on("click", function(e){
        e.preventDefault();
        $(this).parents(".textarea_box").find("textarea").each(function(){
            var textarea = $(this).val() + '\n<a href=""></a>';
            $(this).val(textarea);
        });
    });

    $(".strong_text").on("click", function(e){
        e.preventDefault();
        $(this).parents(".textarea_box").find("textarea").each(function(){
            var textarea = $(this).val() + '\n<strong></strong>';
            $(this).val(textarea);
        });
    });

    $(".select_box.title_box.category_div").each(function(){
        var input = $(this).next("p").html();
        $(this).find("img").on("click", function(){
            $(this).parents(".select_box.title_box.category_div").next("p").append(input);
        });
    });

    $(".select_box.title_box.tags_div").each(function(){
        var input = $(this).next("p").html();
        $(this).find("img").on("click", function(){
            $(this).parents(".select_box.title_box.tags_div").next("p").append(input);
        });
    });

    var tmp_file_inputbox = $(".card-footer div.tmp_file_box").html();
    console.log(tmp_file_inputbox)

    $(".card-footer div.tmp_file_box p img").on("click", function(){
        console.log("click")
        console.log(tmp_file_inputbox)
        $(this).parents("div.tmp_file_box").append(tmp_file_inputbox);
        $(this).parents("div.tmp_file_box").find("p").each(function(index){
            if(index != 0) {
                $(this).remove();
            }
        });
    });

    var url_inputbox = $(".card-footer div.url_box").html();

    $(".card-footer div.url_box p img").on("click", function(){
        $(this).parents(".card-footer").find("div.url_box").append(url_inputbox);
        $(this).parents("div.url_box").find("p").each(function(index){
            if(index != 0) {
                $(this).remove();
            }
        });
    });
});

// 投稿内容の改行、リンク、強調文字を取得変換(str → elem)
$(function(){
    $(document).ready(function(){
        var p_count = [];
        $(".main_article_contents.info").each(function(index){
            $(this).find("p").addClass("block_id_"+index);
        });
        $(".main_article_contents.info").each(function(index){
            $(this).find(".block_id_"+index).each(function(){
                var content = $(this).html(),
                    string = /&lt;strong&gt;(.*?)strong&gt;/,
                    link_value = [],
                    strong = content.split(string);
                try {
                    for (x in strong) {
                        if (strong[x].indexOf("&lt;br&gt;") != -1){
                            var textIndex = strong[x].replace("&lt;br&gt;", "");
                            strong[x] = "<br>" + textIndex + "<br>"
                        }
                        if (strong[x].indexOf("href=") != -1){

                            var link = /&lt;a href=(.*?)a&gt;/,
                                text_link = content.match(/href="(.*?)"/),
                                link_value = [1],
                                link_content = content.split(link);
                            for (y in link_content) {
                                if (link_content[y].indexOf('"'+text_link[1]+'"&gt;') != -1) {
                                    var textLink = link_content[y].replace('"'+text_link[1]+'"&gt;', "").replace("&lt;/", "");
                                    link_content[y] = "<a href="+text_link[1]+" class='textarea_link'>" + textLink + "</a>"
                                }
                                if (link_content[y].indexOf("&lt;br&gt;") != -1){
                                    var textIndex = link_content[y].replace("&lt;br&gt;", "");
                                    link_content[y] = "<br>" + textIndex + "<br>"
                                }
                                if (link_content[y].indexOf("strong") != -1){
                                    var string_other = /&lt;strong&gt;(.*?)strong&gt;/,
                                        strong_other = link_content[y].split(string);
                                    for (z in strong_other) {
                                        if (strong_other[z].indexOf("&lt;/") != -1){
                                            var textIndex = strong_other[z].replace("&lt;/", "");
                                            strong_other[z] = "<strong>"+textIndex+"</strong>"
                                        }
                                    }
                                    link_content[y] = strong_other.join("");
                                }
                            }
                        }
                        if (strong[x].indexOf("&lt;/") != -1){
                            var textIndex = strong[x].replace("&lt;/", "");
                            strong[x] = "<strong>"+textIndex+"</strong>"
                        }
                    }
                } catch {}
                if (link_value.length != 0) {

                    var content = function(){
                        var count = [];
                        for (x in link_content) {
                            count.push(link_content[x]);
                        }
                        var text = count.join("");
                        return text
                    }
                } else {
                    var content = function(){
                        var count = [];
                        for (x in strong) {
                            count.push(strong[x]);
                        }
                        var text = count.join("");
                        return text
                    }
                }
                $(this).html(content());
            });
        });
    });
});

