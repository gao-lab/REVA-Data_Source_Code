<!doctype html>
<?php
    //The function for cal the number of quartile
    function cal_quartile_value($input_array,$n){
        sort($input_array);
        $array_length=count($input_array);
        $qn_pos=1+($array_length-1)*$n;
        $qn_pos_int=floor($qn_pos);
        $qn_pos_float=$qn_pos-$qn_pos_int;
        $qn=$input_array[$qn_pos_int-1]+$qn_pos_float*($input_array[$qn_pos_int]-$input_array[$qn_pos_int-1]);
        return $qn;
    }

    //The function for cal quartile and get outlier
    function cal_quartile($input_array,$feature_array,$category){
        //get data for boxplot
        $q1=cal_quartile_value($input_array,0.25);
        $q2=cal_quartile_value($input_array,0.50);
        $q3=cal_quartile_value($input_array,0.75);
        $iqr=$q3-$q1;
        $lower=$q1-1.5*$iqr;
        $upper=$q3+1.5*$iqr;
        
        $data_for_boxplot=array($lower,$q1,$q2,$q3,$upper);
        
        //get outlier
        $outlier=array();
        $i=0;
        foreach($feature_array as $x=>$x_value){
            if($x_value>$upper or $x_value<$lower){
                $outlier[$i]=[$category,$x_value,$x];
                $i++;
            }		
        }
        return array($data_for_boxplot,$outlier);
    }

    //The function to find index in an array
    function find_index($target_array,$target_element){
        $target_array=array_flip($target_array);
        $finded=$target_array[$target_element];
        if($finded){
            return $finded;
        }else{
            return 0;
        }
    }

    $inter_id=$_GET['id'];#get inter_id from URL
    //connect to annotation database
    $m =new MongoClient("");
    $db=$m->emdb;
    $annotate_collection=$db->data_experiment_anno;
    //query in annotation
    $query_command=array("Id_38" => $anno_id);
    $result_anno=$annotate_collection->findOne($query_command);
    $annotation=$result_anno['Annotation'];
    #check whether the annotation exist
    if(count($annotation)!=0){
        //get cell line
        $cell_line=fopen("./include/cell_line.txt","r");
        $j=0;
        while(!feof($cell_line)){
            $cell_line_name=explode("\n",fgets($cell_line))[0];
            $cell_name[$j]=$cell_line_name;
            $cell_name_id[$j]=array($cell_line_name,$j);
            $j++;
        }
        fclose($cell_line);
        $var_cell_id=find_index($cell_name,$result["Cell_line"]);
        $cell_name=json_encode($cell_name,JSON_UNESCAPED_UNICODE);
        $cell_name_id=json_encode($cell_name_id,JSON_UNESCAPED_UNICODE);
        //get feature name
        $annotation_for_table_all=array();
        $feature_name=fopen("./include/2403_feature.txt","r");
        $j=0;
        while(!feof($feature_name)){
            $feature_item_all=explode("\n",fgets($feature_name))[0];
            $annotation_with_name[$feature_item_all]=$annotation[$j];
            if(explode("|",$feature_item_all)[2]=="None"){
                $feature_item=explode("|",$feature_item_all)[1];
            }else{
                $feature_item=explode("|",$feature_item_all)[1]." (".explode("|",$feature_item_all)[2].")";
            }
            $feature_list[$j]=$feature_item;
            array_push($annotation_for_table_all,array(explode("|",$feature_item_all)[0],$feature_item,$annotation[$j]));
            $j++;
        }
        fclose($feature_name);
        //prepare data for table
        $annotation_for_table=array(array_slice($annotation_for_table_all,0,280),array_slice($annotation_for_table_all,280,1249),array_slice($annotation_for_table_all,1529,766),array_slice($annotation_for_table_all,2295,108));
        $annotation_for_table=json_encode($annotation_for_table,JSON_UNESCAPED_UNICODE);
        //category by cell line
        $cell_line_pos=fopen("./include/pos_by_cell_line.txt","r");
        $data_by_cell=array();
        $j=0;
        while(!feof($cell_line_pos)){
            $cell_pos=explode(",",explode("\n",fgets($cell_line_pos))[0]);
            $tmp_array=array();
            $a=0;
            $b=0;
            $c=0;
            $d=0;
            for($x=0;$x<count($cell_pos);$x++){
                if($cell_pos[$x]<280){
                    array_push($tmp_array,array(0,$a,(float)$annotation[$cell_pos[$x]],$feature_list[$cell_pos[$x]]));
                    $a=$a+1;
                }elseif($cell_pos[$x]<1529){
                    array_push($tmp_array,array(1,$b,(float)$annotation[$cell_pos[$x]],$feature_list[$cell_pos[$x]]));
                    $b=$b+1;
                }elseif($cell_pos[$x]<2295){
                    array_push($tmp_array,array(2,$c,(float)$annotation[$cell_pos[$x]],$feature_list[$cell_pos[$x]]));
                    $c=$c+1;
                }else{
                    array_push($tmp_array,array(3,$d,(float)$annotation[$cell_pos[$x]],$feature_list[$cell_pos[$x]]));
                    $d=$d+1;
                }
            }
            $data_by_cell[$j]=$tmp_array;
            $j=$j+1;
        }
        $data_by_cell=json_encode($data_by_cell,JSON_UNESCAPED_UNICODE);
        
        //slice annotation
        $DNase=array_slice($annotation,0,280);
        $DNase_with_name=array_slice($annotation_with_name,0,280);
        $DNase_data=cal_quartile($DNase,$DNase_with_name,0);

        $tf=array_slice($annotation,280,1249);
        $tf_with_name=array_slice($annotation_with_name,280,1249);
        $tf_data=cal_quartile($tf,$tf_with_name,1);

        $histone=array_slice($annotation,1529,766);
        $histone_with_name=array_slice($annotation_with_name,1529,765); //there is a repeat in histone feature.
        $histone_data=cal_quartile($histone,$histone_with_name,2);

        $methylation=array_slice($annotation,2295,108);
        $methylation_with_name=array_slice($annotation_with_name,2294,108);
        $methylation_data=cal_quartile($methylation,$methylation_with_name,3);

        $anno_array=array($DNase_data[0],$tf_data[0],$histone_data[0],$methylation_data[0]);
        $anno_data=json_encode($anno_array,JSON_UNESCAPED_UNICODE);

        $outlier_array=array_merge($DNase_data[1],$tf_data[1],$histone_data[1],$methylation_data[1]);
        $outlier_data=json_encode($outlier_array,JSON_UNESCAPED_UNICODE);

        $pc=array_slice($annotation,2403,13);
        $evolution=array_slice($annotation,2416,8);
        //21 features
        $feature_title_file=fopen("./include/21_feature.txt","r");
        $pc_data=array();
        $evolution_data=array();
        $i=0;
        while(!feof($feature_title_file)){
            $name=explode("\n",fgets($feature_title_file))[0];
            if($i>12){
                $evolution_data[$i-13]=array($name,$evolution[$i-13]);
            }else{
                $name_abbr=explode("\t",$name)[0];
                $name_full=explode("\t",$name)[1];
                $pc_data[$i]=array($name_abbr,$name_full,$pc[$i]);
            }
            $i++;
        }
        fclose($feature_title_file);
        $pc_data=json_encode($pc_data,JSON_UNESCAPED_UNICODE);
        $evolution_data=json_encode($evolution_data,JSON_UNESCAPED_UNICODE);
    }else{
        $pc_data="0";
        $evolution_data="0";
        $cell_name="0";
        $data_by_cell="0";
        $anno_data="0";
        $outlier_data="0";
    }

?>

<html>
<head>
<title>Annotation Visualization</title>
<link rel="stylesheet" href="css/bootstrap.css">
<link rel="stylesheet" href="css/datatables.css">
<style>
td.highlight {
    background-color:seashell !important;
    cursor:pointer;
}
</style>
</head>
<body>
<h5>
    Chromatin Profile
</h5>
<div class="row" style="margin-left:20px;margin-bottom:30px">
    <div class="col-md-8">
        <div id="anno_chart" style="width: 100%;height:600px;margin-left:50px;"></div>
    </div>
    <div class="col-md-4">
        <div id="annotation_label"><h6>DNA Accessibility</h6></div>
        <table id="profile_table" class="table table-striped table-bordered" style="width:100%">
            <thead>
                <tr>
                    <th>Cell line / Tissue</th>
                    <th>Feature</th>
                    <th>Log fold change</th>
                </tr>
            </thead>
        </table>
    </div>
</div>
<div class="row" style="margin-left:20px;margin-bottom:30px">
    <div class="col-md-8">
        <div id="heat_chart" style="width: 100%;height:450px;"></div><br>
    </div>
    <div class="col-md-4">
        <table id="cell_table" class="table table-striped table-bordered" style="width:100%">
            <thead>
                <tr>
                    <th>Cell line / Tissue</th>
                    <th>ID</th>
                </tr>
            </thead>
        </table>
    </div>
</div>
<h5>
    <i class="fa fa-caret-right"></i> DNA Physicochemical Properties and Evolutionary Features
</h5>
<div class="row" style="margin-left:20px;margin-bottom:30px">
    <div class="col-md-5">
        <h6>DNA Physicochemical Properties</h6>
        <table id="pc_table" class="table table-striped table-bordered" style="width:100%">
            <thead>
                <tr>
                    <th>Feature</th>
                    <th>Full</th>
                    <th>Value</th>
                </tr>
            </thead>
        </table>
    </div>
    <div class="col-md-5">
        <h6>Evolutionary Features</h6>
        <table id="evolution_table" class="table table-striped table-bordered" style="width:100%">
            <thead>
                <tr>
                    <th>Feature</th>
                    <th>Value</th>
                </tr>
            </thead>
        </table>
    </div>
</div>

<script src="js/jquery-3.3.1.min.js" ></script>
<script src="js/jquery.ss.menu.js"></script>
<script src="js/datatables.min.js"></script>
<script src="js/echarts.min.js"></script>
<script>
$(document).ready(function(){
    var pc_data=<?php echo($pc_data);?>;
    var evolution_data=<?php echo($evolution_data);?>;
    var category_list=['Accessibility','TF','Histone','Methylation'];
    var cell_name=<?php echo($cell_name);?>;
    var cell_name_id=<?php echo($cell_name_id);?>;
    var hp_data=<?php echo($data_by_cell);?>;
    var var_cell_id=<?php echo($var_cell_id);?>;
    var annotation_for_table=<?php echo($annotation_for_table);?>;

    function heat_map_v(hp_data,cell_name,category_list,cell_id){
        data=hp_data[cell_id];
        data=data.map(function(item){
            return [item[1],item[0],item[2],item[3]];
        });

        var heat_chart=echarts.init(document.getElementById('heat_chart'));
        var heat_chart_option={
            title:[
                {
                    text:'Chromatin Profile Feature Heatmap by Cell Line / Tissue',
                    left:'center'
                }
            ],
            toolbox:{
                left:'90%',
                feature:{
                    saveAsImage:{
                        title:'Save as image',
                        pixelRatio:3,
                    },
                    restore:{
                        title:'Reset',
                    }
                }
            },
            grid: {
                left: '5%',
                right: '4%',
                bottom: '70px',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                splitArea: {
                    show: true
                },
                axisLabel:{
                    show:false
                }
            },
            yAxis: {
                type: 'category',
                name: cell_name[cell_id],
                nameTextStyle:{
                    fontWeight:'bold',
                },
                data: category_list,
                splitArea: {
                    show: true
                }
            },
            dataZoom: [
                {
                    type: 'slider',
                    xAxisIndex: 0,
                    start: 0,
                    end: 100,
                    bottom:40
                },
            ],
            visualMap: {
                min: -2,
                max: 2,
                precision:2,
                calculable: true,
                dimension:2,
                itemHeight:200,
                orient: 'horizontal',
                left: 'center',
                bottom: '0',
                inRange: {
                    color: ['#3333ff','#ffffcc','#ff3300']
                }
            },
            series: [{
                name: 'Annotation',
                type: 'heatmap',
                data: data,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }],
            tooltip: {
                    position: 'top',
                    formatter:function(param){
                        return param.data[3]+":<br>"+param.data[2];
                    }
            }
        };
        heat_chart.setOption(heat_chart_option);
    }
    heat_map_v(hp_data,cell_name,category_list,var_cell_id);

    var cell_table=$('#cell_table').DataTable({
        "dom": '<"top"f>rt<"bottom"p><"clear">',
        "data":cell_name_id,
        "lengthMenu": [7],
        "processing": true,
        "autoWidth" : true,
        "searching":true,
        "paging":true,
        "columnDefs":[
            {
                "visible":false,
                "targets":[1]
            }
        ],
        "order": [[0, "asc"]],
        "language": {
            "processing": "Processing data...",
            "loadingRecords": "Loading data...",
            "info": "Showing  _START_ to _END_ results, _TOTAL_ results in total ",
        },
        "columns":[
            null,
            null
        ],
    });
    //link cell table and heatmap chart
    $('#cell_table').on("click","tr",function(){
        var id_data=cell_table.row(this).data()[1];
        heat_map_v(hp_data,cell_name,category_list,id_data);
    });

    $('#cell_table tbody')
    .on( 'mouseenter', 'td', function () {
        $(cell_table.cells().nodes() ).removeClass( 'highlight' );
        $(cell_table.cells(this).nodes() ).addClass( 'highlight' );
    })
    .on( 'mouseleave', function () {
        $( cell_table.cells().nodes() ).removeClass( 'highlight' );
    });

    //anno table
    function show_profile(annotation_for_table,category_name){
        if(category_name=="DNA Accessibility"){
            profile_data=annotation_for_table[0];
        }else if(category_name=="TF"){
            profile_data=annotation_for_table[1];
        }else if(category_name=="Histone"){
            profile_data=annotation_for_table[2];
        }else{
            profile_data=annotation_for_table[3];
        }
        //empty datatable
        if($('#profile_table').hasClass('dataTable')){
            var oldTable=$('#profile_table').DataTable();
            oldTable.clear();
            oldTable.destroy();
        }
        //draw table
        var profile_table=$('#profile_table').DataTable({
            "dom": '<"top"f>rt<"bottom"p><"clear">',
            "data":profile_data,
            "lengthMenu": [6],
            "processing": true,
            "autoWidth" : true,
            "searching":true,
            "paging":true,
            "order": [[0, "asc"]],
            "language": {
                "processing": "Processing data...",
                "loadingRecords": "Loading data...",
                "info": "Showing  _START_ to _END_ results, _TOTAL_ results in total ",
            },
            "columns":[
                null,
                null,
                null,
            ],
        });
    }
    show_profile(annotation_for_table,"DNA Accessibility");
    //anno chart
    var anno_chart=echarts.init(document.getElementById('anno_chart'));
    var anno_data=<?php echo($anno_data);?>;
    var outlier_data=<?php echo($outlier_data);?>;
    var anno_chart_option={
        title:[
            {
                text: 'Chromatin Profile Feature Plot',
                left: 'center',
            },
            {
                text: 'Upper: Q3 ＋ 1.5 * IQR \nLower: Q1 － 1.5 * IQR',
                borderColor: '#999',
                borderWidth: 1,
                textStyle: {
                fontSize: 14
            },
                left: '10%',
                top: '90%'
            }
        ],
        tooltip: {
            trigger: 'item',
            axisPointer: {
                type: 'shadow'
                }
        },
        toolbox:{
            left:'88%',
            bottom:50,
            feature:{
                saveAsImage:{
                    title:'Save as image',
                }
            }
        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
        xAxis:{
            type:'category',
            data:["DNA Accessibility","TF","Histone","Methylation"],
            boundaryGap:true,
            nameGap:30,
            axisLabel:{
                rotate:0,
            }
        },
        yAxis:{
            type:'value',
            name:'Log fold change',
            nameLocation:'end',
            nameGap:20,
            splitArea:{
                show:true
                }
        },
        series:[
            {
                name:'boxplot',
                type:'boxplot',
                data:anno_data,
                tooltip: {
                    formatter: function (param) {
                        return [
                            'Feature ' + param.name + ': ',
                            'upper: ' + param.data[5],
                            'Q3: ' + param.data[4],
                            'median: ' + param.data[3],
                            'Q1: ' + param.data[2],
                            'lower: ' + param.data[1]
                        ].join('<br/>');
                    }
                },
            },
            {
                name: 'outlier',
                type: 'scatter',
                data: outlier_data,
                tooltip: {
                    formatter: function (param) {
                        return [
                            'Feature ' + param.name + ': ',
                            param.data[2],
                            param.data[1]
                        ].join('<br/>');
                    }
                },
            }
        ]
    };
    anno_chart.setOption(anno_chart_option);
    //link box plot chart and profile table
    anno_chart.on('click',function(params){
        show_profile(annotation_for_table,params.name)
        $("#annotation_label").html("<h6>"+params.name+"</h6>");
    });
    //pc feature
    var pc_table=$('#pc_table').DataTable({
        "dom": 'rt<"clear">',
        "data":pc_data,
        "processing": true,
        "autoWidth" : true,
        "searching":false,
        "paging":false,
        "columnDefs":[
            {
                "render":function(data,type,row){
                    return "<span title=\""+row[1]+"\">"+data+"</span>";
                },
                "targets":0
            },
            {
                "visible":false,
                "targets":[1]
            }
        ],
        "order": [[0, "asc"]],
        "language": {
            "processing": "Processing data...",
            "loadingRecords": "Loading data...",
            "info": "Showing  _START_ to _END_ results, _TOTAL_ results in total ",
        },
        "columns":[
            null,
            null,
            null
        ],
    });
    //evolution feature
    var evolution_table=$('#evolution_table').DataTable({
        "dom": 'rt<"clear">',
        "data":evolution_data,
        "processing": true,
        "autoWidth" : true,
        "searching":false,
        "paging":false,
        "order": [[0, "asc"]],
        "language": {
            "processing": "Processing data...",
            "loadingRecords": "Loading data...",
            "info": "Showing  _START_ to _END_ results, _TOTAL_ results in total ",
        },
        
        "columns":[
            null,
            null
        ],
    });
});

</script>
</body>
</html>