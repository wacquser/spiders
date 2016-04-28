import re
from bs4 import BeautifulSoup

def extract_info(each):
    '''
    用来提取每一个可点击的标签名和文件名
    :param each: BeautifulSoup解析出来的节点元素
    :return:
    '''
    a_selector = each.find('a')
    id_label = re.findall('id="(treeZhiBiao_\d{0,3}_a)"', str(a_selector), re.S)[0]
    file_name = re.findall('title="(.*?)"', str(a_selector), re.S)[0]
    return id_label,file_name

def extraction(html_file, result_file):
    '''
    用来处理html的页面信息，提取全部可点击的标签名和文件名，并保存到另一个文件中
    :param html_file:   网页的源代码
    :param result_file: 保存结果的文件
    :return:
    '''
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        li_level1_selector = soup.find_all('li',attrs={'class':'level1'}) # 选出全部一级标签
        for each in li_level1_selector:
            l1_id_label, l1_dir_name = extract_info(each)
            li_level2_selector = each.find_all('li',attrs={'class':'level2'}) # 选出全部二级标签
            with open(result_file, 'a+', encoding='utf-8') as result:
                result.write(l1_id_label + '\n') # 写入一级标签
                for each in li_level2_selector:
                    l2_id_label, l2_dir_name = extract_info(each)
                    li_level3_selector = each.find_all('li') # 检测是否存在三级标签
                    if li_level3_selector:
                        result.write(l2_id_label + '\n')
                        for each in li_level3_selector:
                            l3_id_label, l3_file_name = extract_info(each)
                            file_name = l1_dir_name+'/'+l2_dir_name+'/'+l3_file_name+'.xls'
                            result.write(l3_id_label+' '+ file_name+'\n')
                        result.write('\n')
                    else:
                        file_name = l1_dir_name +'/' + l2_dir_name+'.xls'
                        result.write(l2_id_label + ' ' + file_name + '\n')
                result.write('\n')

if __name__ == '__main__':
    extraction('source.html', 'intermediate.txt')