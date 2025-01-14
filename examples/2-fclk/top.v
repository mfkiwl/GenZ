// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps
 
module top(
	input clk,
	output [3:0]led,
	input [1:0]sw
    );
	wire [3:0]FCLK_CLK_unbuffered;
	wire [3:0]FCLK_CLK_buffered;
	BUFG FCLK_CLK_0_BUFG (.I(FCLK_CLK_unbuffered[0]), .O(FCLK_CLK_buffered[0]));
	BUFG FCLK_CLK_1_BUFG (.I(FCLK_CLK_unbuffered[1]), .O(FCLK_CLK_buffered[1]));
	BUFG FCLK_CLK_2_BUFG (.I(FCLK_CLK_unbuffered[2]), .O(FCLK_CLK_buffered[2]));
	BUFG FCLK_CLK_3_BUFG (.I(FCLK_CLK_unbuffered[3]), .O(FCLK_CLK_buffered[3]));

	PS7 PS7_inst (
	.FCLKCLK			    (FCLK_CLK_unbuffered),
	.FCLKRESETN			    () // software programmable reset, unused in most cases
	);

	reg [31:0]cnt0 = 0;
	always @ (posedge FCLK_CLK_buffered[0]) begin
		cnt0 <= cnt0 + 1;
	end
	reg [31:0]cnt1 = 0;
	always @ (posedge FCLK_CLK_buffered[1]) begin
		cnt1 <= cnt1 + 1;
	end
	reg [31:0]cnt2 = 0;
	always @ (posedge FCLK_CLK_buffered[2]) begin
		cnt2 <= cnt2 + 1;
	end
	reg [31:0]cnt3 = 0;
	always @ (posedge FCLK_CLK_buffered[3]) begin
		cnt3 <= cnt3 + 1;
	end
	assign led = {cnt3[27], cnt2[27], cnt1[27], cnt0[27]};
endmodule

