import os
import numpy as np
import bisect
os.chdir(os.path.dirname(__file__))
with open('input.txt') as f:
    light_info_list=f.read().strip().split('\n')

total_button_presses=0
row_count=0
for light_info in light_info_list:
    row_count+=1
    light_diagram,rest=light_info.split(']')
    N_lights=len(light_diagram)-1
    button_str,joltage_requirement=rest.split('{')
    joltage_requirement=np.array([int(j) for j in joltage_requirement[:-1].split(',')]).astype(int)
    button_list=[]
    button_indices_list=[]
    button_press_limits=dict()
    for i,bs in enumerate(button_str.strip().split()):
        button=np.zeros(N_lights).astype(int)
        press_limit=1e20
        for b in bs.strip('()').split(','):
            int_b=int(b)
            button[int_b]=1
            press_limit=min(press_limit,joltage_requirement[int_b])
        button_press_limits[i]=press_limit
        button_list.append(button)
        button_indices_list.append(i)
    N_buttons=len(button_list)

    system_matrix=np.array(button_list).T
    iterate=True
    if N_buttons==N_lights:
        try:
            superposition_coefficients=np.linalg.solve(system_matrix,joltage_requirement)
            min_presses=sum(superposition_coefficients)
            iterate=False
        except:
            pass
    if iterate:
        unique_row_tuples=set()
        for row,j in zip(system_matrix,joltage_requirement):
            unique_row_tuples.add((tuple(row),j))
        import sympy as sp
        sp_system_matrix=sp.Matrix(system_matrix)
        sp_rhs=sp.Matrix(joltage_requirement)
        sp_system=sp_system_matrix.row_join(sp_rhs)
        reduced, _ = sp_system.rref()
        reduced_system_matrix,reduced_rhs=np.array(reduced[:,:-1]),np.array(reduced[:,-1])

        constants=dict()
        sorted_system_list=[]
        for row,rhs in zip(reduced_system_matrix,reduced_rhs):
            rhs=rhs[0]
            zero_count=0
            min_r=1e20
            for r in row:
                if r==0:
                    zero_count+=1
                else:
                    min_r=min(min_r,r)
            if zero_count==N_buttons:
                continue
            if zero_count==N_buttons-1:
                constants[row.argmax()]=rhs
                continue
            bisect.insort(sorted_system_list,(zero_count,row,rhs),key=lambda x:x[0])
        sorted_system_list=sorted_system_list[::-1]

        dependent_lamba_strs=dict()
        indpendents=[]
        eq_count=0
        for _,row,rhs in sorted_system_list:
            dependent_indices=[]
            independent_indices=[]
            new_independent_indices=[]
            lhs_found=False
            lhs_index=-1
            for i,val in enumerate(row):
                if val!=0:
                    if i in dependent_lamba_strs:
                        dependent_indices.append((i,val))
                    elif i in indpendents:
                        independent_indices.append((i,val))
                    else:
                        if not lhs_found:
                            lhs_index=(i,val)
                            lhs_found=True
                        else:
                            new_independent_indices.append((i,val))
            if lhs_index==-1:
                print('something wrong!') #for own attempt at matrix reduction
                continue
            #initial "simpler" version which could result in non-integer values due to float-point inaccuracies
            # divisor=lhs_index[1]
            # lambda_str=f"{rhs/divisor}-("
            # for i,val in dependent_indices:
            #     lambda_str+=f"{val/divisor}*{dependent_lamba_strs[i]}+"
            # for i,val in independent_indices:
            #     lambda_str+=f"{val/divisor}*independent_variables_dict[{i}]+"
            # for i,val in new_independent_indices:
            #     lambda_str+=f"{val/divisor}*independent_variables_dict[{i}]+"
            #     indpendents.append(i)
            # lambda_str=lambda_str[:-1]+')'

            #to avoid flot-point issues, multiply with denominator and carry out additions first and then do the division
            lambda_str=f"({rhs.numerator}-("
            for i,val in dependent_indices:
                lambda_str+=f"{val*rhs.denominator}*{dependent_lamba_strs[i]}+"
            for i,val in independent_indices:
                lambda_str+=f"{val*rhs.denominator}*independent_variables_dict[{i}]+"
            for i,val in new_independent_indices:
                lambda_str+=f"{val*rhs.denominator}*independent_variables_dict[{i}]+"
                indpendents.append(i)
            lambda_str=lambda_str[:-1]+f'))/{rhs.denominator*lhs_index[1]}'
            dependent_lamba_strs[lhs_index[0]]=lambda_str

        if len(indpendents)==0:
            min_presses=0
            joltage_comparison=0*joltage_requirement
            for i,val in constants.items():
                joltage_comparison=joltage_comparison+val*button_list[i]
                min_presses+=val
        else:
            dependent_lamba_dict=dict()
            for i,_str in dependent_lamba_strs.items():
                dependent_lamba_dict[i]=eval(f"lambda : {_str}")
            independent_variables_dict={i:0 for i in indpendents}
            independent_variables_list=list(independent_variables_dict.keys())
            last_index=len(independent_variables_list)-1

            min_presses=1e20
            max_iter=max(joltage_requirement)
            
            valid=True
            it=0
            max_count=0
            max_count_stop=last_index+1
            finished=False
            increment=False
            while not finished:
                if it!=last_index:
                    if increment:
                        if independent_variables_dict[independent_variables_list[it]]<button_press_limits[independent_variables_list[it]]:
                            independent_variables_dict[independent_variables_list[it]]+=1
                            for i in range(it+1,last_index+1):
                                independent_variables_dict[independent_variables_list[i]]=0
                            it+=1
                            increment=False
                        else:
                            it-=1
                    else:
                        it+=1
                else:
                    press_sum=0
                    valid=True
                    joltage_comparison=0*joltage_requirement
                    button_presses_dict={}
                    for i,dependent_lambda in dependent_lamba_dict.items():
                        val=dependent_lambda()
                        if val<0 or val%1!=0:
                            valid=False
                            break
                        joltage_comparison=joltage_comparison+val*button_list[i]
                        button_presses_dict[i]=val
                        press_sum+=val
                    if valid:
                        for i,val in constants.items():
                            joltage_comparison=joltage_comparison+val*button_list[i]
                            button_presses_dict[i]=val
                            press_sum+=val
                        for i,val in independent_variables_dict.items():
                            press_sum+=val
                            joltage_comparison=joltage_comparison+val*button_list[i]
                            button_presses_dict[i]=val
                        if np.sum(np.abs(joltage_comparison-joltage_requirement))==0:
                            min_presses=min(min_presses,press_sum)
                    if independent_variables_dict[independent_variables_list[last_index]]<button_press_limits[independent_variables_list[last_index]]:
                        independent_variables_dict[independent_variables_list[last_index]]+=1
                    else:
                        finished=True
                        for i,val in independent_variables_dict.items():
                            if val!=button_press_limits[i]:
                                finished=False
                                break
                        if not finished:
                            it-=1
                            increment=True

        ####

        #own attempt at matrix reduction, fails when the reduced system-matrix should contain fractions
        #-equation-equivalent of inserting one equation into another and the same parameter appears on LHS and RHS
        # #reduce system matrix
        # while True:
        #     system_list=[]
        #     system_rhs=[]
        #     for row,j in unique_row_tuples:
        #         system_list.append(np.array(row))
        #         system_rhs.append(j)
            
        #     unique_row_tuples=set()
        #     subtracted_count=0
        #     for i,row in enumerate(system_list):
        #         to_subtract=system_list[:i]+system_list[i+1:]
        #         jr=system_rhs[:i]+system_rhs[i+1:]
        #         subtracted=False
        #         for row_,j in zip(to_subtract,jr):
        #             subtraction=row-row_
        #             if subtraction.min()==0:
        #                 subtracted=True
        #                 break
        #         if subtracted:
        #             unique_row_tuples.add((tuple(subtraction),system_rhs[i]-j))
        #             subtracted_count+=1
        #         else:
        #             unique_row_tuples.add((tuple(row),system_rhs[i]))
        #     if subtracted_count==0:
        #         break
        # # for r in system_matrix:
        # #     print(r)
        # # print(' ')
        # # for r,r_ in unique_row_tuples:
        # #     print(np.array([int(__r) for __r in r]),int(r_))
        # # print('--')
        # #identify constants and order rows according to number of non-zero elements in the system matrix/list
        # constants=dict()
        # sorted_system_list=[]
        # for row,rhs in zip(system_list,system_rhs):
        #     row_sum=sum(row)
        #     if row_sum==1:
        #         constants[row.argmax()]=rhs
        #     else:
        #         bisect.insort(sorted_system_list,(row_sum,row,rhs),key=lambda x:x[0])
        # #set dependent and independent variables + assign lambdas to assign values to dependent variables
        # dependent_lamba_strs=dict()
        # indpendents=[]
        # eq_count=0
        # indpendents_dict={}
        # for _,row,rhs in sorted_system_list:
        #     dependent_indices=[]
        #     independent_indices=[]
        #     new_independent_indices=[]
        #     lhs_found=False
        #     lhs_index=-1
        #     print(row)
        #     for i,val in enumerate(row):
        #         print(independent_indices,dependent_indices)
        #         if val==1:
        #             if i in dependent_lamba_strs:
        #                 dependent_indices.append(i)
        #             elif i in indpendents:
        #                 independent_indices.append(i)
        #                 try:
        #                     indpendents_dict[eq_count].append(i)
        #                 except:
        #                     indpendents_dict[eq_count]=[i]
        #             else:
        #                 if not lhs_found:
        #                     lhs_index=i
        #                     lhs_found=True
        #                 else:
        #                     new_independent_indices.append(i)
        #                     try:
        #                         indpendents_dict[eq_count].append(i)
        #                     except:
        #                         indpendents_dict[eq_count]=[i]
        #     if lhs_index==-1:
        #         print('something wrong!')
        #         continue
        #     lambda_str=f"{rhs}-("
        #     for i in dependent_indices:
        #         lambda_str+=f"{dependent_lamba_strs[i]}+"
        #     for i in independent_indices:
        #         lambda_str+=f"independent_variables_dict[{i}]+"
        #     for i in new_independent_indices:
        #         lambda_str+=f"independent_variables_dict[{i}]+"
        #         indpendents.append(i)
        #     lambda_str=lambda_str[:-1]+')'
        #     dependent_lamba_strs[lhs_index]=lambda_str
        # eq_count+=1
        
        # if len(indpendents)==0:
        #     min_presses=0
        #     joltage_comparison=0*joltage_requirement
        #     for i,val in constants.items():
        #         joltage_comparison=joltage_comparison+val*button_list[i]
        #         min_presses+=val
        #     if np.sum(np.abs(joltage_comparison-joltage_requirement))!=0:
        #         1
        # else:
        #     dependent_lamba_dict=dict()
        #     for i,_str in dependent_lamba_strs.items():
        #         dependent_lamba_dict[i]=eval(f"lambda : {_str}")
        #         1
        #     independent_variables_dict={i:0 for i in indpendents}
        #     independent_variables_list=list(independent_variables_dict.keys())
        #     last_index=len(independent_variables_list)-1

        #     min_presses=1e20
        #     max_iter=max(joltage_requirement)
        #     #sista index
        #     valid=True
        #     it=0
        #     max_count=0
        #     max_count_stop=last_index+1
        #     finished=False
        #     increment=False
        #     while not finished:
        #         if it!=last_index:
        #             if increment:
        #                 if independent_variables_dict[independent_variables_list[it]]<max_iter:
        #                     independent_variables_dict[independent_variables_list[it]]+=1
        #                     for i in range(it+1,last_index+1):
        #                         independent_variables_dict[independent_variables_list[i]]=0
        #                     it+=1
        #                     increment=False
        #                 else:
        #                     it-=1
        #             else:
        #                 it+=1
        #         else:
        #             press_sum=0
        #             valid=True
        #             joltage_comparison=0*joltage_requirement
        #             button_presses_dict={}
        #             for i,dependent_lambda in dependent_lamba_dict.items():
        #                 val=dependent_lambda()
        #                 if val<0:
        #                     valid=False
        #                     break
        #                 joltage_comparison=joltage_comparison+val*button_list[i]
        #                 button_presses_dict[i]=val
        #                 press_sum+=val
        #             if valid:
        #                 for i,val in constants.items():
        #                     joltage_comparison=joltage_comparison+val*button_list[i]
        #                     button_presses_dict[i]=val
        #                     press_sum+=val
        #                 for i,val in independent_variables_dict.items():
        #                     press_sum+=val
        #                     joltage_comparison=joltage_comparison+val*button_list[i]
        #                     button_presses_dict[i]=val
        #                 if np.sum(np.abs(joltage_comparison-joltage_requirement))==0:
        #                     min_presses=min(min_presses,press_sum)
        #             if independent_variables_dict[independent_variables_list[last_index]]<max_iter:
        #                 independent_variables_dict[independent_variables_list[last_index]]+=1
        #             else:
        #                 max_count+=1
        #                 if max_count==max_count_stop:
        #                     finished=True
        #                 else:
        #                     it-=1
        #                     increment=True
        #     if min_presses==1e20:
        #         print(row_count,N_buttons,N_lights)
    total_button_presses+=min_presses    
    # print(row_count,':',min_presses,total_button_presses)
print("2nd:",int(total_button_presses))

"""
Initial notes (swe):

reducera överbestämda ekvationssystem och iterera lösningar
1. sätt upp systemmatris, stacka buttons i matrix och transponera, varje rad=ekv för varje joltage requirement
-om är kvadratisk och ej reducerbara rader kan lösa direkt
2. reducera rader i matris:
-först utgå från 1a rad och testa subtrahera nedanstående rad från den, om ej får negativ komponent är ok
--lägg då reducerade rad i ny lista som sen blir nästa systemmatris, subtrahera då även 2a element från svarsvektor från 1a element i svarsvektor
-om får negativ komponent, gå vidare till nästa rad
-då är klar m rad 1, gå vidare till rad 2 och försök subtrahera från rad 3 ...
3. om matrisen reducerades, upprepa 2. med den nya matrisen
4. sortera rader i matris efter 3. (och motsvarande element i svarsvektor) efter hur många 1:or har (färre överst)
-plocka ut rader med bara en 1:a, dessa har fixa värden, lägg i separat vektor/dict/...
--index där singel 1:a var som key i dict och värde är motsvarande element i svarsvektorn
5. loopa igenom rader i matris från 4.
-för varje rad, utgå från först påträffade 1:a, denna blir beroende variabel
--index för denna 1:a som key i dict för beroende variabler
--value blir str på form: "svarsvektor_element-vec[index_1]-vec[index_2]-..."
---där vec kommer motsvara en vektor med värden för alla koefficienter då itererar (konstanta, beroende och oberoende parametrar)
---index_1 osv är index för de ettor som påträffades efter den första
--NOTERA: behöver kolla att index för första påträffade 1:a ej finns i beroende_variabel_dict eller kontant_dict
---om så är fallet, gå vidare till nästa 1:a (repetera samma check) och lägg vec[index_0]-... i value där index_0 osv motsvarar index för oberoende samt konstanta
--då satt ihop value str, kolla om några av index finns i beroende-/konstant-dict, ersätt i sånt fall dessa med uttryck/värden från dict
---efter ersatt, gå igenom str och kolla efter symboler som upprepas och förenkla -kanske lättast att göra allra sist så ej behöver implementera check för *?
6. för beroende variabler, skapa lista med lambda-fkner:
-för varje entry i beroende-dict, gör:
-- _list.append(eval("lambda:"+beroende_dict_item_str))
7. assigna värden av oberoende variabler (ex. som nedan)
-efter att alla oberoende variabler är assignade, utvärdera alla lambda-fkn.er för att få värden på beroende variabler
-addera oberoende, konstanta och beroende variabler för att få totalsumman av knapptryck
--spara minimivärdet
-fortsätt att öka oberoende variabler (en i taget) tills att någon beroende variabel blir negativ
--öka då föregående oberoende variabel och nollställ kommande och upprepa
-efter att ej kan öka första oberoende något mer ska ha loopat igenom alla möjliga valid kombinationer
--minimivärdet av knapptryck bör då vara korrekt

initiera alla oberoende variabler som 0

kan assigna värden av oberoende variabler rekursivt
-input index för parameter att öka
-efter ökat utvärdera beroende variabler
-om ingen beroende variabel är negativ, kalla rekursiv funktion igen m nästa index att öka
-då kommer till sista indexet summera vec (alla koefficienter) och jfr med min_värde, om mindre spara som nytt min_värde
-fkn returnerar true om kunde jfr och om ej hade negativ beroende variabel, annars false
-om rekursivt anrop får tillbaka true gör nytt rekusivt anrop för nästa beroende variabel
-om rekursivt anrop får tillbaka false
hålla koll på föregårnde bool för att se om behöver öka sitt egna värde?
varje rekursion sparar referens av koefficienter innan börjar göra rekursiva anrop
-om får tillbaka false, kolla om värde i nästkommande beroende index är 1 steg högre än motsvarade referenskoefficient
--vet då att kunde öka minst 1 gång och ska därför öka sitt egna värde, sätta efterkommande beroende variabler till 0 och göra nytt anrop
"""