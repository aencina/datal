Data Source
```
<dataSource>
	<DataStructure>
		<Field id="table0">
			<type/>
			<format>
				<languaje/>
				<country/>
				<style/>
			</format>
			<Table>
				<Field id="column0">
					<alias/>
					<type/>
					<format>
						<languaje/>
						<country/>
						<style/>
					</format>
				</Field>
				<Field id="column1">
					<alias/>
					<type/>
					<format>
						<languaje/>
						<country/>
						<style/>
					</format>
				</Field>
				<Field id="column2">
					<alias/>
					<type/>
					<format>
						<languaje/>
						<country/>
						<style/>
					</format>
				</Field>
			</Table>
		</Field>
	</DataStructure>
</dataSource>
```



# Select Statement


## Full Table
```
<selectStatement>
	<Select>
		<Column>*</Column>
	</Select>
	<From>
		<Table>table0</Table>
	</From>
	<Where/>
</selectStatement>
```

## Coumna A, C, Fila 2 y 3
```
<selectStatement>
	<Select>
		<Column>column0</Column>
		<Column>column2</Column>
	</Select>
	<From>
		<Table>table0</Table>
	</From>
	<Where>
		<Filter>
			<Operand1>rownum</Operand1>
			<LogicalOperator>00</LogicalOperator>
			<Operand2>1</Operand2>
		</Filter>
		<Filter>
			<Operand1>rownum</Operand1>
			<LogicalOperator>00</LogicalOperator>
			<Operand2>2</Operand2>
		</Filter>
	</Where>
</selectStatement>
```

## Celdas B2, C2, A3
```
<selectStatement>
	<Select>
		<Column>cell4</Column>
		<Column>cell5</Column>
		<Column>cell6</Column>
	</Select>
	<From>
		<Table>table0</Table>
	</From>
	<Where/>
</selectStatement>
```

Seleccionado primera fila como header
```
<dataSource>
	<DataStructure>
		<Field id="table0">
			<Headers>
				<Row>row0</Row>
			</Headers>
			<type/>
			<format>
				<languaje/>
				<country/>
				<style/>
			</format>
			<Table>
				<Field id="column0">
					<alias/>
					<type/>
					<format>
						<languaje/>
						<country/>
						<style/>
					</format>
				</Field>
				<Field id="column1">
					<alias/>
					<type/>
					<format>
						<languaje/>
						<country/>
						<style/>
					</format>
				</Field>
				<Field id="column2">
					<alias/>
					<type/>
					<format>
						<languaje/>
						<country/>
						<style/>
					</format>
				</Field>
			</Table>
		</Field>
	</DataStructure>
</dataSource>
```

Solo se pueden agregar filtros cuando se seleccionan columnas completas, no cuando se filtra por fila
```
<selectStatement>
	<Select>
		<Column>column0</Column>
		<Column>column1</Column>
	</Select>
	<From>
		<Table>table0</Table>
	</From>
	<Where>
		<Filter>
			<Operand1>column2</Operand1>
			<LogicalOperator>00</LogicalOperator>
			<Operand2>parameter0</Operand2>
		</Filter>
	</Where>
</selectStatement>
```

El parámetro creado se envia al guardar así
parameters-0-name:nombreparam
parameters-0-position:0
parameters-0-description:descparam
parameters-0-default:valorparam
parameters-TOTAL_FORMS:1
parameters-INITIAL_FORMS:0

Los tags se envian 
tags-0-name:dasda
tags-1-name:asdasd
tags-TOTAL_FORMS:2
tags-INITIAL_FORMS:0

y los sources
sources-0-name:unafuente
sources-0-url:http://google.com
sources-TOTAL_FORMS:1
sources-INITIAL_FORMS:0