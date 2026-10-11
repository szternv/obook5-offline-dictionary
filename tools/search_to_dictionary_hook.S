.set noreorder
.set noat
.set mips32r2
.text
.globl hook
.ent hook
hook:
    # Replacement body for QtApplicationWindow::search(QString const&)
    # for the tested intermediate libeinkfbreader build.
    lui     $gp, 0x000e
    addiu   $gp, $gp, -0x7dc4
    addu    $gp, $gp, $t9

    addiu   $sp, $sp, -0x30
    sw      $ra, 0x2c($sp)
    sw      $gp, 0x10($sp)
    sw      $s0, 0x28($sp)
    sw      $s1, 0x24($sp)
    sw      $s2, 0x20($sp)

    move    $s0, $a0
    move    $s1, $a1

    # private helper pointer in extended .bss
    lw      $s2, -0x3850($gp)
    bnez    $s2, have_helper
    nop

    # operator new(sizeof(DictFetchScrWord))
    lw      $t9, -0x5f60($gp)
    addiu   $a0, $zero, 0x28
    jalr    $t9
    nop
    lw      $gp, 0x10($sp)
    move    $s2, $v0

    # DictFetchScrWord(QWidget*)
    lw      $t9, -0x72e4($gp)
    move    $a0, $s2
    move    $a1, $s0
    jalr    $t9
    nop
    lw      $gp, 0x10($sp)
    sw      $s2, -0x3850($gp)

have_helper:
    # DictFetchScrWord::searchWord(QString const&)
    lw      $t9, -0x594c($gp)
    move    $a0, $s2
    move    $a1, $s1
    jalr    $t9
    nop
    lw      $gp, 0x10($sp)

    lw      $ra, 0x2c($sp)
    lw      $s0, 0x28($sp)
    lw      $s1, 0x24($sp)
    lw      $s2, 0x20($sp)
    jr      $ra
    addiu   $sp, $sp, 0x30
.end hook
