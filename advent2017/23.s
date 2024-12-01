	.file	"23.c"
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
	subl	$48, %esp
	call	___main
	movl	$1, 24(%esp)
	movl	$0, 44(%esp)
	movl	$0, 40(%esp)
	movl	$0, 36(%esp)
	movl	$0, 20(%esp)
	movl	$0, 32(%esp)
	movl	$0, 16(%esp)
	movl	$0, 28(%esp)
	movl	$57, 44(%esp)
	movl	44(%esp), %eax
	movl	%eax, 40(%esp)
	cmpl	$0, 24(%esp)
	je	L2
	movl	44(%esp), %eax
	imull	$100, %eax, %eax
	addl	$100000, %eax
	movl	%eax, 44(%esp)
	movl	44(%esp), %eax
	addl	$17000, %eax
	movl	%eax, 40(%esp)
L2:
	movl	$1, 32(%esp)
	movl	$2, 36(%esp)
	movl	$2, 20(%esp)
	movl	$2, 36(%esp)
	jmp	L3
L6:
	movl	44(%esp), %eax
	cltd
	idivl	36(%esp)
	movl	%edx, %eax
	testl	%eax, %eax
	jne	L4
	movl	$0, 32(%esp)
	jmp	L5
L4:
	addl	$1, 36(%esp)
L3:
	movl	36(%esp), %eax
	imull	36(%esp), %eax
	cmpl	44(%esp), %eax
	jl	L6
L5:
	cmpl	$0, 32(%esp)
	jne	L7
	addl	$1, 28(%esp)
L7:
	movl	40(%esp), %eax
	movl	44(%esp), %edx
	subl	%eax, %edx
	movl	%edx, %eax
	movl	%eax, 16(%esp)
	addl	$17, 44(%esp)
	cmpl	$0, 16(%esp)
	jne	L2
	movl	28(%esp), %eax
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
	.globl	_original_main
	.def	_original_main;	.scl	2;	.type	32;	.endef
_original_main:
LFB11:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$56, %esp
	movl	$1, -28(%ebp)
	movl	$0, -12(%ebp)
	movl	$0, -32(%ebp)
	movl	$0, -16(%ebp)
	movl	$0, -36(%ebp)
	movl	$0, -20(%ebp)
	movl	$0, -40(%ebp)
	movl	$0, -24(%ebp)
	movl	$57, -12(%ebp)
	movl	-12(%ebp), %eax
	imull	$100, %eax, %eax
	addl	$100000, %eax
	movl	%eax, -12(%ebp)
	movl	-12(%ebp), %eax
	addl	$17000, %eax
	movl	%eax, -32(%ebp)
L15:
	movl	$1, -20(%ebp)
	movl	$2, -16(%ebp)
	movl	$2, -36(%ebp)
	movl	$2, -16(%ebp)
	jmp	L10
L13:
	movl	-12(%ebp), %eax
	cltd
	idivl	-16(%ebp)
	movl	%edx, %eax
	testl	%eax, %eax
	jne	L11
	movl	$0, -20(%ebp)
	jmp	L12
L11:
	addl	$1, -16(%ebp)
L10:
	movl	-16(%ebp), %eax
	imull	-16(%ebp), %eax
	cmpl	-12(%ebp), %eax
	jl	L13
L12:
	cmpl	$0, -20(%ebp)
	jne	L14
	addl	$1, -24(%ebp)
L14:
	movl	-32(%ebp), %eax
	movl	-12(%ebp), %edx
	subl	%eax, %edx
	movl	%edx, %eax
	movl	%eax, -40(%ebp)
	addl	$17, -12(%ebp)
	cmpl	$0, -40(%ebp)
	jne	L15
	movl	-24(%ebp), %eax
	movl	%eax, 4(%esp)
	movl	$LC0, (%esp)
	call	_printf
	movl	$0, %eax
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
LFE11:
	.ident	"GCC: (GNU) 4.8.1"
	.def	_printf;	.scl	2;	.type	32;	.endef
