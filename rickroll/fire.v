module my_code #(
    parameter int WIDTH = 640,
    parameter int HEIGHT = 480,
    parameter int CONSOLE_COLUMNS = WIDTH / 8,
    parameter int CONSOLE_ROWS    = HEIGHT / 8
)(
    input  logic clk,
    input  logic rst,

    input  int px,
    input  int py,
    input  logic hsync,
    input  logic vsync,

    input  int col,
    input  int row,

    output int char,
    output logic [23:0] foreground_color,
    output logic [23:0] background_color
);

    // Fire resolution: 80x60 → scaled to 640x480
    localparam int FW = 80;
    localparam int FH = 60;

    logic [7:0] fire[FH-1:0][FW-1:0];

    logic old_vsync;
    logic [7:0] lfsr = 8'hA5;
    logic [3:0] spark_div; // slows sparks ~10x

    assign char = 0;
    assign foreground_color = 24'hFFFFFF;

    // Scale VGA pixel to fire coordinates
    wire [6:0] fx = px[9:3]; // /8 → 0..79
    wire [5:0] fy = py[9:3]; // /8 → 0..59

    always_comb begin
        logic [7:0] v;
        v = fire[fy][fx];
        background_color = {v, v >> 1, v >> 3};
    end

    integer x, y;
    always_ff @(posedge clk) begin
        if (rst) begin
            old_vsync <= 0;
            lfsr <= 8'hA5;
            spark_div <= 0;
            for (y = 0; y < FH; y = y + 1)
                for (x = 0; x < FW; x = x + 1)
                    fire[y][x] <= 0;
        end else begin
            if (!vsync && old_vsync) begin
                // propagate fire upward
                for (y = 0; y < FH-1; y = y + 1)
                    for (x = 0; x < FW; x = x + 1)
                        fire[y][x] <= fire[y+1][x] - (x & 1);

                // slow sparks (≈ every 10 frames)
                spark_div <= spark_div + 1;
                if (spark_div == 0) begin
                    // LFSR
                    lfsr <= {lfsr[6:0],
                             lfsr[7]^lfsr[5]^lfsr[4]^lfsr[3]};

                    // bottom-row sparks
                    fire[FH-1][lfsr[6:0] % FW] <= 8'hFF;
                end
            end
            old_vsync <= vsync;
        end
    end

endmodule
