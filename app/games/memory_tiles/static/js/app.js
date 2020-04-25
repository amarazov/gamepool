// Memory Game
// 2014 Nate Wiley
// License -- MIT
// best in full screen, works on phones/tablets (min height for game is 500px..) enjoy ;)
// Follow me on Codepen

function start_play(typ) {

    var Memory = {

        init: function (cards) {
            this.$game = $(".game");
            this.$modal = $(".modal");
            this.$overlay = $(".modal-overlay");
            this.$restartButton = $("button.restart");
            this.cardsArray = $.merge(cards, cards);
            this.start = new Date();
            this.moves = 0;
            this.shuffleCards(this.cardsArray);
            this.setup();
        },

        shuffleCards: function () {
            this.$cards = $(this.shuffle(this.cardsArray));
        },

        setup: function () {
            this.html = this.buildHTML();
            this.$game.html(this.html);
            this.$memoryCards = $(".card");
            this.moves = 0;
            this.start = new Date();
            this.paused = false;
            this.guess = null;
            this.binding();
        },

        binding: function () {
            this.$memoryCards.on("click", this.cardClicked);
            this.$restartButton.on("click", $.proxy(this.reset, this));
        },
        // kinda messy but hey
        cardClicked: function () {
            var _ = Memory;
            let $card = $(this);
            if (!_.paused && !$card.find(".inside").hasClass("matched") && !$card.find(".inside").hasClass("picked")) {
                _.moves++;
                console.log(_.moves);
                $card.find(".inside").addClass("picked");
                if (!_.guess) {
                    _.guess = $(this).attr("data-id");
                } else if (_.guess == $(this).attr("data-id") && !$(this).hasClass("picked")) {
                    $(".picked").addClass("matched");
                    _.guess = null;
                } else {
                    _.guess = null;
                    _.paused = true;
                    setTimeout(function () {
                        $(".picked").removeClass("picked");
                        Memory.paused = false;
                    }, 600);
                }
                if ($(".matched").length == $(".card").length) {
                    _.win();
                }
            }
        },

        win: function () {
            this.paused = true;

            let postData = {
                game_name:'memory_tiles.game',
                game_typ:typ,
                time:Math.round((new Date() - Memory.start)/1000),
                args: JSON.stringify({
                    moves: Memory.moves
                }),
            };
            $.ajax({
                url: '/games/_post_answer/',
                contentType: 'application/JSON',
                data: JSON.stringify(postData),
                type: 'POST',
                success: function () {
                    setTimeout(function () {window.location.replace('/next_game/')}, TIMEOUT);
                },
                error: function (error) {
                    console.log(error);
                }
            });
            setTimeout(function () {
                Memory.showModal();
                Memory.$game.fadeOut();
            }, 1000);
        },

        showModal: function () {
            this.$overlay.show();
            this.$modal.fadeIn("slow");
        },

        hideModal: function () {
            this.$overlay.hide();
            this.$modal.hide();
        },

        reset: function () {
            this.hideModal();
            this.shuffleCards(this.cardsArray);
            this.setup();
            this.$game.show("slow");
        },

        // Fisher--Yates Algorithm -- https://bost.ocks.org/mike/shuffle/
        shuffle: function (array) {
            var counter = array.length, temp, index;
            // While there are elements in the array
            while (counter > 0) {
                // Pick a random index
                index = Math.floor(Math.random() * counter);
                // Decrease counter by 1
                counter--;
                // And swap the last element with it
                temp = array[counter];
                array[counter] = array[index];
                array[index] = temp;
            }
            return array;
        },

        buildHTML: function () {
            var frag = '';
            this.$cards.each(function (k, v) {
                frag += '<div class="card" data-id="' + v.id + '"><div class="inside">\
				<div class="front"><img src="' + v.img + '"\
				alt="' + v.name + '" /></div>\
				<div class="back"><img src="/static/games.memory_tiles/img/back.png"\
				alt="Back" /></div></div>\
				</div>';
            });
            return frag;
        }
    };

    let cards = [
        {
            name: "php",
            img: "/static/games.memory_tiles/img/php-logo_1.png",
            id: 1,
        },
        {
            name: "css3",
            img: "/static/games.memory_tiles/img/css3-logo.png",
            id: 2
        },
        {
            name: "html5",
            img: "/static/games.memory_tiles/img/html5-logo.png",
            id: 3
        },
        {
            name: "jquery",
            img: "/static/games.memory_tiles/img/jquery-logo.png",
            id: 4
        },
        {
            name: "javascript",
            img: "/static/games.memory_tiles/img/js-logo.png",
            id: 5
        },
        {
            name: "node",
            img: "/static/games.memory_tiles/img/nodejs-logo.png",
            id: 6
        },
        {
            name: "photoshop",
            img: "/static/games.memory_tiles/img/photoshop-logo.png",
            id: 7
        },
        {
            name: "python",
            img: "/static/games.memory_tiles/img/python-logo.png",
            id: 8
        },
        {
            name: "rails",
            img: "/static/games.memory_tiles/img/rails-logo.png",
            id: 9
        },
        {
            name: "sass",
            img: "/static/games.memory_tiles/img/sass-logo.png",
            id: 10
        },
        {
            name: "sublime",
            img: "/static/games.memory_tiles/img/sublime-logo.png",
            id: 11
        },
        {
            name: "wordpress",
            img: "/static/games.memory_tiles/img/wordpress-logo.png",
            id: 12
        },
    ];

    Memory.init(cards.slice(0, typ));
}
