var squareImgBuffer = 5;
var bodyWidth = document.DO_PAGEWIDTH || document.body.clientWidth;

const VIEW_MODE = $(body).attr("do-view-mode");
const PLATFORM = $(body).attr("do-platform");

var imageOps = {
  pure: {
    isPortrait: function(imgNode) {
      //Make sure the image is larger than the buffer.
      if ($(imgNode).hasClass("thumb")) {
        var naturalHeight = imgNode.getAttribute("naturalHeight");
        var naturalWidth = imgNode.getAttribute("naturalWidth");
        if (naturalHeight - naturalWidth > squareImgBuffer) {
          return true;
        } else {
          return false;
        }
      } else {
        if (imgNode.naturalHeight - imgNode.naturalWidth > squareImgBuffer) {
          return true;
        } else {
          return false;
        }
      }
    },
    isSquare: function(imgNode) {
      //Treat the img still as a square with some buffer pixels.
      //Reason: Day One camera square is off by a couple pixels
      if ($(imgNode).hasClass("thumb")) {
        var naturalHeight = imgNode.getAttribute("naturalHeight");
        var naturalWidth = imgNode.getAttribute("naturalWidth");
        if (Math.abs(naturalHeight - naturalWidth) <= squareImgBuffer) {
          return true;
        } else {
          return false;
        }
      } else {
        if (
          Math.abs(imgNode.naturalHeight - imgNode.naturalWidth) <=
          squareImgBuffer
        ) {
          return true;
        } else {
          return false;
        }
      }
    }
  },

  impure: {
    unwrap: function() {
      var foo = $("p > img").unwrap();
    },

    createInlinedContainer: function(imgA, imgB) {
      const VIEW_MODE = $(body).attr("do-view-mode");
      const TAG_NAME = VIEW_MODE == "print" ? "div" : "img";

      var imgAPath = imgA.src;
      var imgBPath = imgB.src;
      var container = document.createElement("div");
      container.classList.add("inline-img-wrapper");
      var imgAElem = document.createElement(TAG_NAME);
      imgAElem.id = imgA.id;
      if (VIEW_MODE != "print") imgAElem.src = imgAPath;
      if (imgAElem.id == "placeholder") {
        imgAElem.style.backgroundColor = "#e8e8e8";
      } else {
        imgAElem.style.background = 'url("' + imgAPath + '")';
      }
      imgAElem.setAttribute("onclick", "imageTapped('" + imgA.id + "')");
      imgAElem.classList.add("inline-img");
      var imgBElem = document.createElement(TAG_NAME);
      imgBElem.id = imgB.id;
      if (VIEW_MODE != "print") imgBElem.src = imgBPath;
      if (imgBElem.id == "placeholder") {
        imgBElem.style.backgroundColor = "#e8e8e8";
      } else {
        imgBElem.style.background = 'url("' + imgBPath + '")';
      }
      imgBElem.setAttribute("onclick", "imageTapped('" + imgB.id + "')");
      imgBElem.classList.add("inline-img");
      if (imageOps.pure.isPortrait(imgA) && imageOps.pure.isPortrait(imgB)) {
        var ratio = 3 / 2; // Portrait
        container.style.height = ratio * (bodyWidth / 2) + "px";
        container.setAttribute("isportrait", "true");
      } else {
        container.style.height = bodyWidth / 2 + "px";
        container.setAttribute("issquare", "true");
      }

      container.appendChild(imgAElem);
      container.appendChild(imgBElem);
      return container;
    },

    markLargeImages: function() {
      // Get all images on page
      var nodes = document.querySelectorAll("img");
      var allImages = Array.prototype.slice.call(nodes, 0);

      // Get only large images
      var largeImages = allImages.filter(function(node) {
        if (node.id == "placeholder" || $(node).hasClass("thumb")) {
          var naturalWidth = node.getAttribute("naturalWidth");
          return naturalWidth >= 500;
        } else {
          return node.naturalWidth >= 500;
        }
      });

      largeImages.forEach(function(node) {
        node.classList.add("large-image");
      });
    },

    limitImageHeight: function() {
      var maxHeight = bodyWidth;
      var nodes = $("img:not(.inline-img)");
      var isPlaceholder = function(node) {
        if (node.id == "placeholder") {
          return true;
        } else {
          return false;
        }
      };
      var isTallerThanMaxHeight = function(node) {
        if (isPlaceholder(node)) {
          var naturalHeight = node.getAttribute("naturalHeight");
          return naturalHeight > bodyWidth;
        } else {
          return node.naturalHeight > bodyWidth;
        }
      };

      var isPlaceholderSquare = function(node) {
        var naturalHeight = node.getAttribute("naturalHeight");
        var naturalWidth = node.getAttribute("naturalWidth");

        if (Math.abs(naturalHeight - naturalWidth) <= squareImgBuffer) {
          return true;
        } else {
          return false;
        }
      };

      var isPortrait = function(node) {
        if (isPlaceholder(node)) {
          var naturalWidth = node.getAttribute("naturalWidth");
          var naturalHeight = node.getAttribute("naturalHeight");
          return naturalWidth < naturalHeight;
        } else {
          return node.naturalWidth < node.naturalHeight;
        }
      };
      var allImages = Array.prototype.slice.call(nodes, 0);

      var portraitImages = allImages.filter(function(node) {
        return isTallerThanMaxHeight(node) && isPortrait(node);
      });

      var placeholderImages = allImages.filter(function(node) {
        return (
          (isTallerThanMaxHeight(node) ||
            isPlaceholderSquare(node) ||
            isPortrait(node)) &&
          isPlaceholder(node)
        );
      });

      portraitImages.forEach(function(node) {
        node.style.maxHeight = maxHeight + "px";
        node.style.width = "auto";
        node.style.margin = "0 auto";
      });

      placeholderImages.forEach(function(node) {
        node.style.maxHeight = maxHeight + "px";
        node.style.margin = "0 auto";
        node.style.backgroundColor = "#e8e8e8";
        node.style.width = bodyWidth;
        node.style.marginTop = "5px";
        node.style.marginLeft = "-20px";
      });
    },

    makeSideBySide: function() {
      function go(visitedImages) {
        // Get all images on page
        var nodes = document.querySelectorAll(".large-image");
        var allImages = Array.prototype.slice.call(nodes, 0);

        // Ignore those which have already been visited
        var unvisited = allImages.filter(function(i) {
          return !visitedImages.includes(i);
        });

        // If we've visited everything, we're done!
        if (unvisited.length == 0) {
          return;
        }

        // Get the image to operate on, and its immediate sibling image
        var img = unvisited[0];
        var nextImg = img.nextElementSibling;

        // If img doesn't have a sibling, move along
        if (nextImg == null) {
          return go(visitedImages.concat(img));
        }

        // If the two aren't inlinable, add the first to the visited list and move on
        // Make sure the next image is the same. portrait == portrait and not portrait == square
        if (
          nextImg.tagName != "IMG" ||
          (!imageOps.pure.isPortrait(img) &&
            !imageOps.pure.isSquare(nextImg)) ||
          (!imageOps.pure.isSquare(img) && !imageOps.pure.isPortrait(nextImg))
        ) {
          return go(visitedImages.concat(img));
        }

        // Otherwise, remove the next image from the dom,
        // and replace the current image with a div containing
        // the magic inlined image markup
        var inlined = imageOps.impure.createInlinedContainer(img, nextImg);
        nextImg.parentNode.removeChild(nextImg);
        img.parentNode.replaceChild(inlined, img);

        // Looooooop!
        return go(visitedImages.concat(img, nextImg));
      }

      go([]);
    },

    unindentMedia: function() {
      var iframes = document.getElementsByTagName("iframe");

      for (var i = 0; i < iframes.length; ++i) {
        var wrapper = document.createElement("div");
        wrapper.classList.add("media_embed");
        var iframe = iframes[i];
        if (iframe.src && iframe.src.indexOf("youtube") !== -1) {
          wrapper.classList.add("youtube");
        }
        if (iframe.src && iframe.src.indexOf("vimeo") !== -1) {
          wrapper.classList.add("vimeo");
        }
        wrapper.appendChild(iframe.cloneNode(true));
        iframe.parentNode.replaceChild(wrapper, iframe);
        $("iframe").wrap("<p></p>");
      }
    },

    resizeVideos: function() {
      var videoContainers = $(
        ".media_embed.youtube iframe, .media_embed.vimeo iframe"
      );

      videoContainers.height(bodyWidth * (9 / 16));
    }
  }
};

/* wrapPrintHeaders hackily simulates the behavior that we should get (but don't seem to be getting)
with page-break-after: avoid; */
function wrapPrintHeaders() {
  /* We want to keep page breaks from happening between headers and the content immediately follow-
  ing. We reverse the list of headers after selecting it, so that sub-headers are grouped with their
  content before their super-headers get grouped. If you try this without reversing, and you have
  two headers in a row, the second two headers will get grouped together, and the associated content
  will be left ungrouped. */
  var nodes = $(
    $(
      ".entry .header, .entry h1, .entry h2, .entry h3, .entry h4, .entry h5, .entry h6"
    )
      .not(".header h1")
      .get()
      .reverse()
  );

  nodes.each(function(_, node) {
    // Use add this random color as a border to the breakerTag when
    // you want to visually debug what the breakers are doing.
    // var color = '#'+Math.floor(Math.random()*16777215).toString(16);
    var breakerTag =
      "<div class='break-breaker' style='page-break-inside: avoid'/>";
    $(node).next().andSelf().wrapAll(breakerTag);
  });

  /* Also, we want to keep the tags at the end of the entry from ending up all alone on a page */
  $(".tags").toArray().forEach(function(tags) {
    $(tags).prev().andSelf().wrapAll(breakerTag);
  });
}

function destoryIFrames() {
  $("iframe").remove();
}

function markLinksForWhichToShowURL() {
  $("a:not(:contains(http))").addClass("showURL");
}

function removeMarginFromFirstChildren() {
  function go(node) {
    if (node == null) return;
    node.style.marginTop = "0px";
    // Images should but right up to the top, though. This number correlates
    // with the css rule for the body padding in day-one-ios-override.css
    // Also, if we've come across an inline image container, we should scoot
    // that up and not descend into its children.
    if (node.classList.contains("inline-img-wrapper")) {
      node.style.marginTop = "-1.2em";
      return;
    } else if (node.tagName == "IMG") {
      node.style.marginTop = "-1.2em";
    }
    var children = $(node).find(":not(script):not(style)");
    if (children.length == 0) return;
    go(children[0]);
  }

  var mainNode = $("#body")[0];
  go(mainNode);
}

function resizeCheckboxes() {
  var body = document.body;
  var style = window.getComputedStyle(body, null).getPropertyValue("font-size");
  var fontSize = parseFloat(style);

  var checkboxes = document.querySelectorAll("input[type='checkbox']");
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].style.padding = fontSize / 2 + "px";
  }

  //Add in the styles to the stylesheet because its a pseudo-element
  document.styleSheets[0].addRule(
    "ul.checkboxes input[type=checkbox]:checked:after",
    "width: " +
      fontSize +
      "px; height: " +
      fontSize +
      "px; background-size: " +
      fontSize / 2 +
      "px; left: " +
      fontSize / 2 / 2 +
      "px; top:" +
      (fontSize / 2 / 2 + 1) +
      "px;"
  );
}

function convertAudioBlocks() {
  var audioBlocks = document.querySelectorAll("[data-audio]");
  for (var i = 0; i < audioBlocks.length; i++) {
    createAudioElement(audioBlocks[i]);
  }
}

function createAudioElement(audioBlock) {
  // ⚠️🆘DAAAAAAAAAAANGER⚠️🆘
  // ::::::::::::::::::::
  // 🐲 🐉 DOM MUTATION 🐲 🐉
  var player = document.createElement("div");
  player.className += "player";
  var row = document.createElement("div");
  row.className += "row";
  player.appendChild(row);
  var scrubber = document.createElement("div");
  scrubber.className += "scrubber";
  row.appendChild(scrubber);
  var scrubberTimelineContainer = document.createElement("div");
  scrubberTimelineContainer.className += "scrubber-timeline-container";
  scrubber.appendChild(scrubberTimelineContainer);
  var scrubberTimeline = document.createElement("div");
  scrubberTimeline.className += "scrubber-timeline";
  scrubberTimelineContainer.appendChild(scrubberTimeline);
  var scrubberTimelineCurrent = document.createElement("div");
  scrubberTimelineCurrent.className += "scrubber-timeline-current";
  scrubberTimelineContainer.appendChild(scrubberTimelineCurrent);
  var scrubberKnobContainer = document.createElement("div");
  scrubberKnobContainer.className += "scrubber-knob-container";
  scrubber.appendChild(scrubberKnobContainer);
  var scrubberKnob = document.createElement("div");
  scrubberKnob.className += "scrubber-knob";
  scrubberKnobContainer.appendChild(scrubberKnob);
  var currentTime = document.createElement("p");
  currentTime.className += "current-time";
  scrubber.appendChild(currentTime);
  var endTime = document.createElement("p");
  endTime.className += "end-time";
  scrubber.appendChild(endTime);
  var playButton = document.createElement("button");
  playButton.className += "play-button play";
  row.appendChild(playButton);
  var settingsButton = document.createElement("button");
  settingsButton.className += "settings-button";
  row.appendChild(settingsButton);
  if (audioBlock.innerHTML) {
    var innerContainer = document.createElement("div");
    innerContainer.className += "inner-container";
    player.appendChild(innerContainer);
    var transcriptBlurb = document.createElement("div");
    transcriptBlurb.className += "transcript-blurb tb-truncate";
    transcriptBlurb.style.color = "rgb(124, 123, 124)";
    transcriptBlurb.innerHTML = audioBlock.innerHTML;
    innerContainer.appendChild(transcriptBlurb);
    var tbShow = document.createElement("a");
    tbShow.innerHTML = "Show Transcript";
    tbShow.className += "tb-show";
    innerContainer.appendChild(tbShow);
  } else {
    var transcriptBlurb = document.createElement("div");
    transcriptBlurb.style.display = "none";
    var tbShow = document.createElement("a");
    tbShow.style.display = "none";
  }
  var audio = document.createElement("audio");
  audio.className += "audio";
  // Preloads the audio and metadata
  audio.preload = "auto";
  var source = document.createElement("source");
  source.src = audioBlock.dataset.audio;
  source.type = "audio/mp4";
  audio.appendChild(source);
  player.appendChild(audio);

  audioBlock.parentElement.replaceWith(player);
  getWidthOfPlayers(
    true,
    audio,
    playButton,
    scrubberKnobContainer,
    scrubberKnob,
    currentTime,
    endTime,
    scrubberTimeline,
    scrubberTimelineCurrent,
    transcriptBlurb,
    tbShow,
    settingsButton,
    false
  );
}

var scopedScreenWidth;
function getWidthOfPlayers(
  init,
  audio,
  playButton,
  scrubberKnobContainer,
  scrubberKnob,
  currentTime,
  endTime,
  scrubberTimeline,
  scrubberTimelineCurrent,
  transcriptBlurb,
  tbShow,
  settingsButton,
  lastIteration
) {
  var scrubbers = document.getElementsByClassName("scrubber");
  if (init || scopedScreenWidth !== document.body.clientWidth) {
    scopedScreenWidth = document.body.clientWidth;
    if (document.body.clientWidth >= 400) {
      for (var i = 0; i < scrubbers.length; i++) {
        scrubbers[i].className = "scrubber";
        scrubbers[i].className += " scrubber-landscape";
      }
    } else {
      for (var i = 0; i < scrubbers.length; i++) {
        scrubbers[i].className = "scrubber";
        scrubbers[i].className += " scrubber-portrait";
      }
    }
  }
  audioInit(
    init,
    audio,
    playButton,
    scrubberKnobContainer,
    scrubberKnob,
    currentTime,
    endTime,
    scrubberTimeline,
    scrubberTimelineCurrent,
    transcriptBlurb,
    tbShow,
    settingsButton,
    lastIteration
  );
}

var screenWidth;
function audioInit(
  init,
  audio,
  playButton,
  scrubberKnobContainer,
  scrubberKnob,
  currentTime,
  endTime,
  timeline,
  timelineCurrent,
  transcriptBlurb,
  transcriptButton,
  settingsButton,
  lastIteration
) {
  var timelineWidth = timeline.offsetWidth - scrubberKnob.offsetWidth;
  var onScrubber = false;
  var scrubberKnobContainerPadding = "38";

  if (init) {
    screenWidth = document.body.clientWidth;
    // preload doesnt initialize the playhead so timeUpdate doesnt get fired until played.
    audio.play();
    audio.pause();

    scrubberKnobContainer.style.bottom = scrubberKnobContainerPadding + "%";

    var truncateLength = 75;
    if (transcriptBlurb.innerHTML.length >= truncateLength) {
      var truncatedText = document.createElement("p");
      truncatedText.style.margin = "0";
      truncatedText.style.color = "rgb(124, 123, 124)";
      truncatedText.innerHTML =
        transcriptBlurb.innerHTML.substring(0, truncateLength) + "...";
      transcriptBlurb.parentElement.insertBefore(
        truncatedText,
        transcriptBlurb.parentElement.firstChild
      );
      toggleTruncatedText();
    } else {
      transcriptButton.remove();
    }

    function toggleTruncatedText() {
      if (transcriptBlurb.classList.contains("tb-truncate")) {
        truncatedText.style.display = "block";
        transcriptBlurb.style.display = "none";
      } else {
        truncatedText.style.display = "none";
        transcriptBlurb.style.display = "block";
      }
    }

    transcriptButton.addEventListener("click", function() {
      if (transcriptBlurb.classList.contains("tb-truncate")) {
        transcriptBlurb.classList.remove("tb-truncate");
        transcriptButton.innerHTML = "Minimize";
      } else {
        transcriptBlurb.classList.add("tb-truncate");
        transcriptButton.innerHTML = "Show Transcript";
      }
      toggleTruncatedText();
    });

    settingsButton.addEventListener("click", function() {
      var audioId = audio.firstChild.src
        .split("DayOneAudios/")[1]
        .split(".m4a")[0];
      window.location = "audio://" + audioId;
    });

    playButton.addEventListener("click", function() {
      if (audio.paused) {
        audio.play();
        playButton.classList.remove("play");
        playButton.classList.add("pause");
      } else {
        audio.pause();
        playButton.classList.remove("pause");
        playButton.classList.add("play");
      }
    });

    audio.addEventListener("loadedmetadata", function() {
      currentTime.innerHTML = formatTime(audio.currentTime);
      endTime.innerHTML = formatTime(audio.duration);
    });
  }

  function updateTimeline() {
    var playPercent = timelineWidth * (audio.currentTime / audio.duration);
    scrubberKnobContainer.style.left = playPercent + "px";
    timelineCurrent.style.width = playPercent + "px";

    currentTime.innerHTML = formatTime(audio.currentTime);
    if (audio.currentTime == audio.duration) {
      scrubberKnobContainer.style.left = playPercent + 1 + "px";
      playButton.classList.remove("pause");
      playButton.classList.add("play");
    }
  }

  if (init || screenWidth !== document.body.clientWidth) {
    if (lastIteration) {
      screenWidth = document.body.clientWidth;
    }

    updateTimeline();
    audio.addEventListener("timeupdate", updateTimeline);

    scrubberKnobContainer.addEventListener("touchstart", function(e) {
      e.preventDefault();
      onScrubber = true;

      window.addEventListener("touchmove", moveScrubber, true);
      window.addEventListener("touchend", handleEnd, false);
    });

    scrubberKnob.addEventListener("mousedown", function(e) {
      e.preventDefault();
      onScrubber = true;

      window.addEventListener("mousemove", moveScrubber, true);
      window.addEventListener("mouseup", handleEnd, true);
    });
  }

  function returnPercent(e) {
    if (e.changedTouches) {
      return (
        (e.changedTouches[0].clientX - getPosition(timeline)) / timelineWidth
      );
    } else {
      return (e.clientX - getPosition(timeline)) / timelineWidth;
    }
  }

  function handleEnd(e) {
    if (onScrubber == true) {
      moveScrubber(e);
      if (e.type == "touchend") {
        window.removeEventListener("touchmove", moveScrubber, true);
        audio.currentTime = audio.duration * returnPercent(e);
      } else {
        window.removeEventListener("mousemove", moveScrubber, true);
        audio.currentTime = audio.duration * returnPercent(e);
      }
    }
    onScrubber = false;
  }

  function moveScrubber(e) {
    if (e.changedTouches) {
      var newPosLeft = e.changedTouches[0].clientX - getPosition(timeline);
      audio.currentTime = audio.duration * returnPercent(e);
    } else {
      var newPosLeft = e.clientX - getPosition(timeline);
      audio.currentTime = audio.duration * returnPercent(e);
    }

    if (newPosLeft >= 0 && newPosLeft <= timelineWidth) {
      scrubberKnobContainer.style.left = newPosLeft + "px";
    }
    if (newPosLeft < 0) {
      scrubberKnobContainer.style.left = "0px";
    }
    if (newPosLeft > timelineWidth) {
      scrubberKnobContainer.style.left = timelineWidth + 1 + "px";
    }
  }

  function formatTime(seconds) {
    var minutes = Math.floor(seconds / 60);
    seconds = Math.floor(seconds % 60);
    seconds = seconds >= 10 ? seconds : "0" + seconds;
    return minutes + ":" + seconds;
  }

  function getPosition(el) {
    return el.getBoundingClientRect().left;
  }
}

function DOMain() {
  // Order matters here, we're mutating the DOM!
  if (document.querySelectorAll("[data-audio]").length > 0) {
    convertAudioBlocks();
  }
  resizeCheckboxes();
  imageOps.impure.unwrap();
  imageOps.impure.markLargeImages();
  imageOps.impure.makeSideBySide();
  if ($("#placeholder").length) {
    imageOps.impure.limitImageHeight();
  }
  imageOps.impure.unindentMedia();
  imageOps.impure.resizeVideos();
  window.addEventListener("resize", imageOps.impure.resizeVideos);

  if (VIEW_MODE == "read-single" && PLATFORM == "ios") {
    removeMarginFromFirstChildren();
  }

  if (VIEW_MODE == "print") {
    markLinksForWhichToShowURL();
    imageOps.impure.limitImageHeight();
    wrapPrintHeaders();
    destoryIFrames();
  }

  if (document.DO_SCROLLTOPOSITION > 0) {
    scrollTo(0, document.DO_SCROLLTOPOSITION);
  }
}

window.requestAnimationFrame(function check() {
  if (bodyWidth !== document.body.clientWidth) {
    // Rerun things that require bodywidth update.
    bodyWidth = document.body.clientWidth;
    //Initial bodyWidth is wrong so this updates the height of the container
    $(".inline-img-wrapper").each(function() {
      if ($(this).attr("isportrait") == "true") {
        var ratio = 3 / 2; // Portrait
        $(this).height(ratio * (bodyWidth / 2) + "px");
      } else if ($(this).attr("issquare") == "true") {
        $(this).height(bodyWidth / 2 + "px");
      }
    });
  }

  if (document.getElementsByClassName("player").length > 0) {
    var players = document.querySelectorAll(".player");
    for (var i = 0; i < players.length; i++) {
      var audio = players[i].querySelector(".audio");
      var playButton = players[i].querySelector(".play-button");
      var scrubberKnobContainer = players[i].querySelector(
        ".scrubber-knob-container"
      );
      var scrubberKnob = players[i].querySelector(".scrubber-knob");
      var currentTime = players[i].querySelector(".current-time");
      var endTime = players[i].querySelector(".end-time");
      var scrubberTimeline = players[i].querySelector(".scrubber-timeline");
      var scrubberTimelineCurrent = players[i].querySelector(
        ".scrubber-timeline-current"
      );
      var transcriptBlurb = players[i].querySelector(".transcript-blurb");
      var tbShow = players[i].querySelector(".tb-show");
      var settingsButton = players[i].querySelector(".settings-button");
      var lastIteration = false;
      if (players.length - 1 == i) {
        lastIteration = true;
      }

      getWidthOfPlayers(
        false,
        audio,
        playButton,
        scrubberKnobContainer,
        scrubberKnob,
        currentTime,
        endTime,
        scrubberTimeline,
        scrubberTimelineCurrent,
        transcriptBlurb,
        tbShow,
        settingsButton,
        lastIteration
      );
    }
  }

  requestAnimationFrame(check);
});

window.addEventListener("load", DOMain);

window.gotFullResImage = function(data) {
  $("#" + data.id).attr("src", data.src);
};
