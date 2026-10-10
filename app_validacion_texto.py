<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Club Park - Reporte Operativo Semanal</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f9;
            margin: 0;
            padding: 10px;
            color: #212529;
        }
        .container {
            max-width: 480px;
            margin: 0 auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        h2 {
            text-align: center;
            font-size: 1.25rem;
            margin-bottom: 5px;
            color: #2c3e50;
        }
        .subtitle {
            text-align: center;
            font-size: 0.85rem;
            color: #6c757d;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 14px;
        }
        label {
            display: block;
            font-weight: bold;
            font-size: 0.85rem;
            margin-bottom: 5px;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ced4da;
            border-radius: 8px;
            font-size: 1rem;
            box-sizing: border-box;
            background-color: #fff;
        }
        .camera-box {
            border: 2px dashed #0d6efd;
            padding: 12px;
            text-align: center;
            border-radius: 8px;
            background: #f8f9fa;
            margin-bottom: 15px;
        }
        #preview {
            max-width: 100%;
            max-height: 180px;
            margin-top: 10px;
            display: none;
            border-radius: 6px;
        }
        .summary-box {
            background: #e9ecef;
            padding: 12px;
            border-radius: 8px;
            margin: 15px 0;
            font-size: 0.9rem;
        }
        .summary-box div {
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
        }
        .summary-box div:last-child {
            margin-bottom: 0;
            font-weight: bold;
            font-size: 1rem;
            border-top: 1px solid #dee2e6;
            padding-top: 6px;
        }
        button {
            width: 100%;
            background-color: #0d6efd;
            color: white;
            border: none;
            padding: 12px;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 8px;
        }
        .btn-export {
            background-color: #198754;
        }
        .btn-clear {
            background-color: #dc3545;
            font-size: 0.85rem;
            padding: 8px;
            margin-top: 15px;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>CLUB PARK VALET</h2>
    <div class="subtitle">Control Operativo Local (Sin Internet)</div>

    <form id="reportForm">
        <div class="camera-box">
            <label for="foto">📸 Tomar Foto de la Hoja (Evidencia)</label>
            <input type="file" id="foto" accept="image/*" capture="environment" onchange="previewImage(event)">
            <img id="preview" alt="Vista previa">
        </div>

        <div class="form-group">
            <label>Fecha:</label>
            <input type="date" id="fecha" required>
        </div>

        <div class="form-group">
            <label>Unidad / Establecimiento:</label>
            <input type="text" id="unidad" placeholder="Ej. Sushiitto" required>
        </div>

        <div class="form-group">
            <label>Costo del Boleto ($):</label>
            <input type="number" id="costo" value="40" required oninput="calcular()">
        </div>

        <div class="form-group">
            <label>Folio Inicial:</label>
            <input type="number" id="inicial" required oninput="calcular()">
        </div>

        <div class="form-group">
            <label>Folio Final:</label>
            <input type="number" id="final" required oninput="calcular()">
        </div>

        <div class="form-group">
            <label>Boletos Cancelados:</label>
            <input type="number" id="cancelados" value="0" required oninput="calcular()">
        </div>

        <div class="form-group">
            <label>Boletos Pérdidos:</label>
            <input type="number" id="perdidos" value="0" required oninput="calcular()">
        </div>

        <div class="form-group">
            <label>Sueldo del Operador ($):</label>
            <input type="number" id="sueldo" value="280" required oninput="calcular()">
        </div>

        <div class="summary-box">
            <div><span>Total Boletos:</span> <strong id="resTotal">0</strong></div>
            <div><span>Boletos Pagados:</span> <strong id="resPagados">0</strong></div>
            <div><span>Ingreso Bruto:</span> <strong id="resBruto">$0</strong></div>
            <div><span>Ingreso Neto:</span> <strong id="resNeto" style="color: #d9534f;">$0</strong></div>
        </div>

        <button type="button" onclick="guardarRegistro()">💾 Guardar Registro en el Celular</button>
        <button type="button" class="btn-export" onclick="exportarExcel()">📊 Exportar Reporte Semanal (Excel/CSV)</button>
        <button type="button" class="btn-clear" onclick="limpiarDatosGuardados()">🗑️ Borrar Historial Local</button>
    </form>
</div>

<script>
    document.getElementById('fecha').valueAsDate = new Date();

    function previewImage(event) {
        const reader = new FileReader();
        reader.onload = function(){
            const output = document.getElementById('preview');
            output.src = reader.result;
            output.style.display = 'block';
        };
        reader.readAsDataURL(event.target.files[0]);
    }

    function calcular() {
        const inicial = parseInt(document.getElementById('inicial').value) || 0;
        const final = parseInt(document.getElementById('final').value) || 0;
        const cancelados = parseInt(document.getElementById('cancelados').value) || 0;
        const perdidos = parseInt(document.getElementById('perdidos').value) || 0;
        const costo = parseFloat(document.getElementById('costo').value) || 0;
        const sueldo = parseFloat(document.getElementById('sueldo').value) || 0;

        let totalBoletos = (final >= inicial) ? (final - inicial + 1) : 0;
        let pagados = totalBoletos - cancelados - perdidos;
        if (pagados < 0) pagados = 0;

        let bruto = pagados * costo;
        let neto = bruto - sueldo;

        document.getElementById('resTotal').innerText = totalBoletos;
        document.getElementById('resPagados').innerText = pagados;
        document.getElementById('resBruto').innerText = '$' + bruto;
        document.getElementById('resNeto').innerText = '$' + neto;
    }

    function guardarRegistro() {
        const unidad = document.getElementById('unidad').value.trim();
        if (!unidad) {
            alert('Por favor, ingresa el nombre de la unidad.');
            return;
        }

        const registro = {
            fecha: document.getElementById('fecha').value,
            unidad: unidad,
            costo: document.getElementById('costo').value,
            inicial: document.getElementById('inicial').value,
            final: document.getElementById('final').value,
            cancelados: document.getElementById('cancelados').value,
            perdidos: document.getElementById('perdidos').value,
            sueldo: document.getElementById('sueldo').value,
            bruto: document.getElementById('resBruto').innerText,
            neto: document.getElementById('resNeto').innerText
        };

        let registros = JSON.parse(localStorage.getItem('clubpark_semana') || '[]');
        registros.push(registro);
        localStorage.setItem('clubpark_semana', JSON.stringify(registros));

        alert('¡Guardado correctamente en la memoria del teléfono!');
        document.getElementById('reportForm').reset();
        document.getElementById('preview').style.display = 'none';
        document.getElementById('fecha').valueAsDate = new Date();
        calcular();
    }

    function exportarExcel() {
        let registros = JSON.parse(localStorage.getItem('clubpark_semana') || '[]');
        if (registros.length === 0) {
            alert('No hay registros guardados para exportar esta semana.');
            return;
        }

        let csv = "\uFEFFFecha,Unidad,Costo Boleto,Folio Inicial,Folio Final,Cancelados,Perdidos,Sueldo,Ingreso Bruto,Ingreso Neto\n";
        registros.forEach(r => {
            csv += `${r.fecha},${r.unidad},${r.costo},${r.inicial},${r.final},${r.cancelados},${r.perdidos},${r.sueldo},${r.bruto},${r.neto}\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", "Reporte_Semanal_ClubPark.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function limpiarDatosGuardados() {
        if (confirm('¿Deseas borrar todo el historial almacenado en este teléfono?')) {
            localStorage.removeItem('clubpark_semana');
            alert('Historial limpiado.');
        }
    }
</script>

</body>
</html>
