import os
os.chdir(os.path.dirname(__file__))
file='input.txt'
# file='example.txt'
with open(file) as f:
    dataList=f.read().strip().split('\n')


def recursive_check(test_value,eq_list,operator_list=[]):
    value=eq_list.pop()
    if eq_list:
        if test_value%value==0:
            a,op_list_a=recursive_check(test_value//value,eq_list+[],operator_list+['*'])
            if a:
                return a,op_list_a
            
            b,op_list_b=recursive_check(test_value-value,eq_list+[],operator_list+['+'])
            return b,op_list_b
            
        else:
            b,op_list_b=recursive_check(test_value-value,eq_list+[],operator_list+['+'])
            return b,op_list_b
                
    else:
        if value==test_value:
            return True,operator_list
        else:
            return False,operator_list

def recursive_check_2(test_value,eq_list,operator_list=[]):
    value=eq_list.pop()
    if eq_list:
        if test_value%value==0:
            a,op_list_a=recursive_check_2(test_value//value,eq_list+[],operator_list+['*'])
            if a:
                return a,op_list_a
            tv_str=str(test_value)
            v_str=str(value)
            Nv=len(v_str)
            if tv_str[-Nv:]==v_str:
                try:
                    c,op_list_c=recursive_check_2(int(tv_str[:-Nv]),eq_list+[],operator_list+['||'])
                    if c:
                        return c,op_list_c
                except:
                    return False,operator_list
            
            b,op_list_b=recursive_check_2(test_value-value,eq_list+[],operator_list+['+'])
            return b,op_list_b
        else:
            tv_str=str(test_value)
            v_str=str(value)
            Nv=len(v_str)
            if tv_str[-Nv:]==v_str:
                c,op_list_c=recursive_check_2(int(tv_str[:-Nv]),eq_list+[],operator_list+['||'])
                if c:
                    return c,op_list_c
            b,op_list_b=recursive_check_2(test_value-value,eq_list+[],operator_list+['+'])
            return b,op_list_b
                
    else:
        if value==test_value:
            return True,operator_list
        else:
            return False,operator_list

total_calibration_result=0
additional_calibration_result_2=0
for row in dataList:
    test_value,eq=row.split(':')
    test_value=int(test_value)
    eq_list=[int(x) for x in eq.strip().split()]
    check_bool,op_list=recursive_check(test_value,eq_list+[])
    if check_bool:
        total_calibration_result+=test_value
    else:
        check_bool,op_list=recursive_check_2(test_value,eq_list)
        if check_bool:
            additional_calibration_result_2+=test_value

print('1st:',total_calibration_result)
print('2nd:',additional_calibration_result_2+total_calibration_result)
1

