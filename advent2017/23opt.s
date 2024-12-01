	.file	"23opt.c"
	.def	___main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
LC0:
	.ascii "%d\12\0"
	.text
	.globl	_main
	.def	_main;	.scl	2;	.type	32;	.endef
_main:
LFB10:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	andl	$-16, %esp
	subl	$32, %esp
	call	___main
	movl	$0, 20(%esp)
	movl	$57, 28(%esp)
	movl	28(%esp), %eax
	imull	$100, %eax, %eax
	addl	$100000, %eax
	movl	%eax, 28(%esp)
	movl	28(%esp), %eax
	addl	$17000, %eax
	movl	%eax, 16(%esp)
L6:
	movl	$2, 24(%esp)
	jmp	L2
L5:
	movl	28(%esp), %eax
	cltd
	idivl	24(%esp)
	movl	%edx, %eax
	testl	%eax, %eax
	jne	L3
	addl	$1, 20(%esp)
	jmp	L4
L3:
	addl	$1, 24(%esp)
L2:
	movl	24(%esp), %eax
	imull	24(%esp), %eax
	cmpl	28(%esp), %eax
	jle	L5
L4:
	addl	$17, 28(%esp)
	movl	28(%esp), %eax
	cmpl	16(%esp), %eax
	jg	L6
	movl	20(%esp), %eax
	movl	%eax, 4(%esp)
	movl	$LC0, (%esp)
	call	_printf
	movl	$0, %eax
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE10:
	.ident	"GCC: (GNU) 4.8.1"
	.def	_printf;	.scl	2;	.type	32;	.endef
