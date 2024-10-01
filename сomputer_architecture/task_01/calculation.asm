org 100h

section .data
    a dw 5
    b dw 10
    c dw 3
    result dw 0
    msg db 'Result: $'

section .text
    mov ax, [b]      ; Завантажуємо b в ax
    sub ax, [c]      ; Віднімаємо c
    add ax, [a]      ; Додаємо a
    mov [result], ax ; Зберігаємо результат

    ; Виведення повідомлення
    mov dx, msg
    mov ah, 9
    int 21h

    ; Виведення результату
    mov ax, [result]
    call logging.info_num

    ; Завершення програми
    mov ax, 4c00h
    int 21h

logging.info_num:
    ; Проста процедура для виведення числа
    push ax
    push bx
    push cx
    push dx

    mov bx, 10
    mov cx, 0

divide:
    xor dx, dx
    div bx
    push dx
    inc cx
    test ax, ax
    jnz divide

logging.info:
    pop dx
    add dl, '0'
    mov ah, 2
    int 21h
    loop logging.info

    pop dx
    pop cx
    pop bx
    pop ax
    ret