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

    logic updating;
    logic [6:0] ux; // 0..79
    logic [5:0] uy; // 0..58 (we skip last row)

    always_ff @(posedge clk) begin
        if (rst) begin
            updating <= 0;
            ux <= 0;
            uy <= 0;
            old_vsync <= 0;
        end else begin
            // start update on vsync rising edge (enter VBLANK)
            if (vsync && !old_vsync) begin
                updating <= 1;
                ux <= 0;
                uy <= 0;
            end

            if (updating) begin
                fire[uy][ux] <= fire[uy+1][ux] - (ux & 1);

                if (ux == FW-1) begin
                    ux <= 0;
                    if (uy == FH-2) begin
                        updating <= 0; // done
                        uy <= 0;
                    end else begin
                        uy <= uy + 1;
                    end
                end else begin
                    ux <= ux + 1;
                end
            end

            // bottom sparks (slow)
            if (vsync && !old_vsync) begin
                d <= d + 1;
                if (!d) begin
                    l <= {l[6:0],l[7]^l[5]^l[4]^l[3]};
                    fire[FH-1][l[6:0]] <= 8'hFF;
                end
            end

            old_vsync <= vsync;
        end
    end

endmodule
