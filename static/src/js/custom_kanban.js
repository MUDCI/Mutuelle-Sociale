odoo.define('ton_module.KanbanChart', function (require) {
    "use strict";

    var KanbanRenderer = require('web.KanbanRenderer');

    KanbanRenderer.include({
        _render: function () {
            this._super.apply(this, arguments);

            setTimeout(() => {
                this.$el.find(".o_kanban_chart").each(function () {
                    var ctx = this.getContext("2d");

                    // Vérifier si dataset.chartData existe, sinon fournir une valeur par défaut
                    var chartData = {};
                    try {
                        chartData = this.dataset.chartData ? JSON.parse(this.dataset.chartData) : { solde: [0, 0, 0, 0, 0] };
                    } catch (e) {
                        console.error("Erreur JSON dans dataset.chartData :", e);
                    }

                    new Chart(ctx, {
                        type: "line",
                        data: {
                            labels: ["S1", "S2", "S3", "S4", "S5"],
                            datasets: [{
                                label: "Solde",
                                data: chartData.solde || [0, 0, 0, 0, 0],
                                borderColor: "#B48840",
                                backgroundColor: "rgba(180, 136, 64, 0.2)",
                                borderWidth: 2,
                                fill: true,
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: { beginAtZero: true }
                            }
                        }
                    });
                });
            }, 500);
        },
    });
});
