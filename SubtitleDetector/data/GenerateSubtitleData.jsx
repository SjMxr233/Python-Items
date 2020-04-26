//Generate video subtitle dataset in photoshop CC 2015
 app.preferences.rulerUnits = Units.PIXELS;
 option = new PNGSaveOptions();
(function main()
{
    
    var form = Form ();
    var gui = Gui(form);
    gui.show();
    
})()

function Gui(form)
{
    var TextFlag =false;
    var ImageFlag = false;
    function LoadText()
    {
        randomTextFile =File.openDialog('Select file with target',"TextFile:*.txt",false);
        if(randomTextFile!=null)
        {
            randomTextFile.open('r');
            randomText =randomTextFile.read();
            randomText = randomText.split('\n');
            randomTextFile.close();
            form.textPath.text = randomTextFile;
            TextFlag = true;
        }
    }

    function LoadImage()
    {
      targetPath = Folder.selectDialog('Select folder with target');
      if(targetPath!=null)
      {
            imgFiles = targetPath.getFiles (/\.(png|jpg)$/i);
            form.imagePath.text = targetPath;
            ImageFlag = true;
      }
    }

    function Run()
    {
        if(!ImageFlag){alert("please select image folder!");return;}
        if(!TextFlag){alert ("please select text file!");return;}
        if(imgFiles.length >0&&randomText.length>0)
        {
            var outputFolder = Folder(targetPath+'/generated');
            var outputImage =Folder(outputFolder+'/Image');
            var outputLabel = Folder(outputFolder+'/Label');
            if(!outputFolder.exists)  
            {
                outputFolder.create();
                if(!outputImage.exists) outputImage.create();
                if(!outputLabel.exists) outputLabel.create();
            }
                
            var white = new SolidColor();
            white.rgb.hexValue='FFFFFF';
            var fontType=[];
            //内置字体共734,取前30中文样式
            for (var i=0; i<30; i++) {
                fontType.push(app.fonts[i].name);
            }
            for(var i=0;i<imgFiles.length;i++)
            {
                var curFile =imgFiles[i];
                open(curFile);
                var doc = app.activeDocument;
                var DWidth = doc.width;
                var DHeight =  doc.height;
                doc.resizeImage (DWidth, DHeight, 72, ResampleMethod.AUTOMATIC);
                //alert(app.fonts);
                var TextLayer = doc.artLayers.add();
                TextLayer.kind =LayerKind.TEXT;
                TextLayer.textItem.color =white;
                //30-50字体大小
                var randSize =Math.round(Math.random()*20+30);
                TextLayer.textItem.size = randSize;
                var randFontIdx =Math.round(Math.random()*(fontType.length-1));
                TextLayer.textItem.font = fontType[randFontIdx];
                var text = randomText[Math.round(Math.random()*(randomText.length-1))];
                TextLayer.textItem.contents =text;
                align('AdCH');
                align('AdBt');
                TextLayer.translate(0,-30);
                setOutline ();

                var TBounds = doc.activeLayer.bounds;
                var UL = [TBounds[0].value,TBounds[1].value];
                var UR =[TBounds[2].value,TBounds[1].value];
                var BL = [TBounds[0].value,TBounds[3].value];
                var BR =[TBounds[2].value,TBounds[3].value];
                var Label = UL[0]+','+UL[1]+','+UR[0]+','+UR[1]+','+BL[0]+','+BL[1]+','+BR[0]+','+BR[1];
                 
                 //save label
                 var  labelFile= File(outputLabel+"/"+"gt_img_"+(i+1)+".txt");
                 labelFile.encoding='UTF8';
                 labelFile.open('w');
                 labelFile.write(Label);
                 //save image
                 var pngFile = File(outputImage+"/"+"img_"+(i+1)+".png");
                 doc.saveAs(pngFile,option,true,Extension.LOWERCASE);
                 doc.close(SaveOptions.DONOTSAVECHANGES);
            }
        }
    }
    
    form.loadTextButton.onClick = LoadText;
    form.loadImageButton.onClick = LoadImage;
    form.startButton.onClick = Run;
    return form.dialog;
}

function Form(){
    
    var that ={};
    
    that.dialog = new Window("dialog"); 
    that.dialog.text = "AddText"; 
    that.dialog.orientation = "column"; 
    that.dialog.alignChildren = ["center","top"]; 
    that.dialog.spacing = 10; 
    that.dialog.margins = 16; 

    that.panel1 = that.dialog.add("panel", undefined, "Import"); 
    that. panel1.orientation = "column"; 
    that.panel1.alignChildren = ["left","top"]; 
    that.panel1.spacing = 10; 
    that.panel1.margins = 10; 

    that.group1 = that.panel1.add("group", undefined); 
    that.group1.orientation = "row"; 
    that.group1.alignChildren = ["left","center"]; 
    that.group1.spacing = 10; 
    that.group1.margins = 0; 

    that.imagePath = that.group1.add("statictext", undefined, undefined); 
    that.imagePath.text = "ImageFolder"; 
    that.imagePath.preferredSize.width = 400; 

    that.loadImageButton = that.group1.add("button", undefined, "Load.."); 

    that.group2 = that.panel1.add("group", undefined); 
    that.group2.orientation = "row"; 
    that.group2.alignChildren = ["left","center"]; 
    that.group2.spacing = 10; 
    that.group2.margins = 0; 

    that.textPath = that.group2.add("statictext", undefined, "RandomTextFile"); 
    that.textPath.preferredSize.width = 400; 

    that.loadTextButton = that.group2.add("button", undefined, "Load.."); 

    that.group3 = that.dialog.add("group", undefined); 
    that.group3.orientation = "row"; 
    that.group3.alignChildren = ["left","center"]; 
    that.group3.spacing = 10; 
    that.group3.margins = 0; 
        
    that.startButton = that.group3.add("button", undefined,"start"); 

    that.quitButton= that.group3.add("button", undefined, "cancel",{name:"cancel"}); 

     return that;
}

function align(method) { 
        activeDocument.selection.selectAll();
        var desc = new ActionDescriptor();
        var ref = new ActionReference();
        ref.putEnumerated( charIDToTypeID( "Lyr " ), charIDToTypeID( "Ordn" ), charIDToTypeID( "Trgt" ) ); 
        desc.putReference( charIDToTypeID( "null" ), ref ); 
        desc.putEnumerated( charIDToTypeID( "Usng" ), charIDToTypeID( "ADSt" ), charIDToTypeID( method ) );
    try{
        executeAction( charIDToTypeID( "Algn" ), desc, DialogModes.NO ); 
   }catch(e){}
        activeDocument.selection.deselect();
}

function setOutline()
{
    try{
            var idsetd = charIDToTypeID( "setd" );
        var desc188 = new ActionDescriptor();
        var idnull = charIDToTypeID( "null" );
            var ref45 = new ActionReference();
            var idPrpr = charIDToTypeID( "Prpr" );
            var idLefx = charIDToTypeID( "Lefx" );
            ref45.putProperty( idPrpr, idLefx );
            var idLyr = charIDToTypeID( "Lyr " );
            var idOrdn = charIDToTypeID( "Ordn" );
            var idTrgt = charIDToTypeID( "Trgt" );
            ref45.putEnumerated( idLyr, idOrdn, idTrgt );
        desc188.putReference( idnull, ref45 );
        var idT = charIDToTypeID( "T   " );
            var desc189 = new ActionDescriptor();
            var idScl = charIDToTypeID( "Scl " );
            var idPrc = charIDToTypeID( "#Prc" );
            desc189.putUnitDouble( idScl, idPrc, 100.000000 );
            var idFrFX = charIDToTypeID( "FrFX" );
                var desc190 = new ActionDescriptor();
                var idenab = charIDToTypeID( "enab" );
                desc190.putBoolean( idenab, true );
                var idpresent = stringIDToTypeID( "present" );
                desc190.putBoolean( idpresent, true );
                var idshowInDialog = stringIDToTypeID( "showInDialog" );
                desc190.putBoolean( idshowInDialog, true );
                var idStyl = charIDToTypeID( "Styl" );
                var idFStl = charIDToTypeID( "FStl" );
                var idCtrF = charIDToTypeID( "CtrF" );
                desc190.putEnumerated( idStyl, idFStl, idCtrF );
                var idPntT = charIDToTypeID( "PntT" );
                var idFrFl = charIDToTypeID( "FrFl" );
                var idSClr = charIDToTypeID( "SClr" );
                desc190.putEnumerated( idPntT, idFrFl, idSClr );
                var idMd = charIDToTypeID( "Md  " );
                var idBlnM = charIDToTypeID( "BlnM" );
                var idNrml = charIDToTypeID( "Nrml" );
                desc190.putEnumerated( idMd, idBlnM, idNrml );
                var idOpct = charIDToTypeID( "Opct" );
                var idPrc = charIDToTypeID( "#Prc" );
                desc190.putUnitDouble( idOpct, idPrc, 100.000000 );
                var idSz = charIDToTypeID( "Sz  " );
                var idPxl = charIDToTypeID( "#Pxl" );
                desc190.putUnitDouble( idSz, idPxl, 1.000000 );
                var idClr = charIDToTypeID( "Clr " );
                    var desc191 = new ActionDescriptor();
                    var idRd = charIDToTypeID( "Rd  " );
                    desc191.putDouble( idRd, 0.000000 );
                    var idGrn = charIDToTypeID( "Grn " );
                    desc191.putDouble( idGrn, 0.000000 );
                    var idBl = charIDToTypeID( "Bl  " );
                    desc191.putDouble( idBl, 0.000000 );
                var idRGBC = charIDToTypeID( "RGBC" );
                desc190.putObject( idClr, idRGBC, desc191 );
                var idoverprint = stringIDToTypeID( "overprint" );
                desc190.putBoolean( idoverprint, false );
            var idFrFX = charIDToTypeID( "FrFX" );
            desc189.putObject( idFrFX, idFrFX, desc190 );
        var idLefx = charIDToTypeID( "Lefx" );
        desc188.putObject( idT, idLefx, desc189 );
        executeAction( idsetd, desc188, DialogModes.NO );
    }catch(e){
        throw(e);
    }
}
