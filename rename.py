import os
import xml.etree.ElementTree as ET

def trans_fanhao(input_string):
    index_of_first_digit = next((i for i, char in enumerate(input_string) if char.isdigit()), None)
    if index_of_first_digit is not None:
        letters_part = input_string[:index_of_first_digit]
        numbers_part = input_string[index_of_first_digit:]
        result_string = f"{letters_part}-{numbers_part}"
        return result_string
    else:
        return input_string

def is_Caribbeancom(str):
    if str[0].isdigit():
        return True
    return False

if __name__=='__main__':
    try:
        actor_ls=os.listdir('./JAV_output')
        for actor in actor_ls:
            av_ls=os.listdir('./JAV_output/'+actor)
            for av in av_ls:
                if(is_Caribbeancom(av)):continue
                SO_flag=av.endswith('SO')
                all_file_ls=os.listdir('./JAV_output/'+actor+'/'+av)
                nfo_file_name= [f1 for f1 in all_file_ls if f1.endswith('.nfo')][0]
                rename_file_name = [f1 for f1 in all_file_ls if f1.startswith(av)]
                nfo_path='./JAV_output/'+actor+'/'+av+'/'+nfo_file_name
                tree = ET.parse(nfo_path)
                root = tree.getroot()
                fix_lst=[".//title",".//originaltitle",".//sorttitle",".//outline",".//plot",".//num"]
                for fix in fix_lst:
                    c=root.find(fix)
                    if c is None:continue
                    old_str=c.text
                    if SO_flag:
                        new_str = old_str.replace(av, trans_fanhao(av[:-2]))
                    else:
                        new_str=old_str.replace(av,trans_fanhao(av))
                    c.text=new_str
                tree.write(nfo_path, encoding="utf-8", xml_declaration=True)
                for re in rename_file_name:
                    if SO_flag:
                        os.rename('./JAV_output/' + actor + '/' + av + '/' + re,
                                './JAV_output/' + actor + '/' + av + '/' + re.replace(av,trans_fanhao(av[:-2])))
                    else:
                        os.rename('./JAV_output/'+actor+'/'+av+'/'+re,'./JAV_output/'+actor+'/'+av+'/'+trans_fanhao(re))
                if SO_flag:
                    os.rename('./JAV_output/' + actor + '/' + av, './JAV_output/' + actor + '/' + trans_fanhao(av[:-2]))
                else:
                    os.rename('./JAV_output/'+actor+'/'+av,'./JAV_output/'+actor+'/'+trans_fanhao(av))
                print('complite '+av)
    except Exception as e:
        print(e)
    input("按任意键退出")



