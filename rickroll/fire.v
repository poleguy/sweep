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

    // version 1
    // Fire resolution: 80x60 → scaled to 640x480
    localparam int FW = 80;
    localparam int FH = 60;

    logic [7:0] fire[FH-1:0][FW-1:0];

    logic old_vsync;
    logic [7:0] lfsr;
    logic [3:0] spark_div;

    logic updating;
    logic [6:0] ux;
    logic [5:0] uy;

    assign char = 0;
    assign foreground_color = 24'hFFFFFF;

    // Scale VGA pixel to fire coordinates
    wire [6:0] fx = px[9:3]; // /8 → 0..79
    wire [5:0] fy = py[9:3]; // /8 → 0..59

    wire [7:0] v = fire[fy][fx];
    assign background_color = {v, v >> 1, v >> 3};

    integer x,y;

    always_ff @(posedge clk) begin
        if (rst) begin
            old_vsync <= 0;
            updating <= 0;
            ux <= 0;
            uy <= 0;
            spark_div <= 0;
            lfsr <= 8'hA5;

          //  for (y=0; y<FH; y=y+1)
          //      for (x=0; x<FW; x=x+1)
          //          fire[y][x] <= 0;
        end else begin
            // start update on vsync rising edge (enter VBLANK)
            if (vsync && !old_vsync) begin
                updating <= 1;
                ux <= 0;
                uy <= 0;
            end

            // scroll fire upward across many clocks
            if (updating) begin
                fire[uy][ux] <= fire[uy+1][ux] - (ux & 1);

                if (ux == FW-1) begin
                    ux <= 0;
                    if (uy == FH-2) begin
                        updating <= 0;
                        uy <= 0;
                    end else begin
                        uy <= uy + 1;
                    end
                end else begin
                    ux <= ux + 1;
                end
            end

            // bottom sparks (slow, only when not updating)
            if (vsync && !old_vsync && !updating) begin
                spark_div <= spark_div + 1;
                if (!spark_div) begin
                    lfsr <= {lfsr[6:0],
                             lfsr[7]^lfsr[5]^lfsr[4]^lfsr[3]};
                    fire[FH-1][lfsr[6:0]] <= 8'hFF;
                end
            end

            old_vsync <= vsync;
        end
    end
endmodule
