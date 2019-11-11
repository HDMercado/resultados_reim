var stacked3Data = {
        labels: [
            {% if game_time %}
            {% for user in game_time %}
                '{{user.name}}',
            {% endfor%}
            {% endif%}
            ],
        datasets: [
            {
                label: "Correctas",
                backgroundColor: 'rgba(82,123,255,100)',
                borderColor: "rgba(60,106,255,100)",
                pointBorderColor: "#fff",
                data: [
            {% if correcta_quantity %}
            {% for user in correcta_quantity %}
                '{{user.quantity}}',
            {% endfor%}
            {% endif%}
            ]
            },
            {
                label: "Incorrectas",
                backgroundColor: 'rgba(240,66,49,94)',
                borderColor: "rgba(240,39,29,94)",
                pointBorderColor: "#fff",
                data: [
            {% if incorrecta_quantity %}
            {% for user in incorrecta_quantity %}
                '{{user.quantity}}',
            {% endfor%}
            {% endif%}
            ]
            }
        ]
    };

    var stacked3Options = {
        responsive: true,
        scales: {
            xAxes:[{
                stacked3:true,
            }],
            yAxes:[{
                stacked3:true,
            }]

        },
        display: true
    };


    var ctx = document.getElementById("stacked3").getContext("2d");
    new Chart(ctx, {type: 'horizontalBar', data: stacked3Data, options:stacked3Options});
    </script>