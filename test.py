with open('./data/单选错题本.txt', 'a+', encoding='utf-8') as f:
    f.write(str(8) + '\n')
    # 读取文件里的行数
    print(f.readlines()) # 为什么输出[]?, 因为上面的写操作已经将文件指针移动到了文件末尾
    # print(f'count_wrong: {count_wrong}')