export const WORLD_FOCUS_GENERAL_VECTOR_AXIS_COUNT = 11;
export const WORLD_FOCUS_HIGH_RISK_VECTOR_AXIS_COUNT = 7;

export const WORLD_FOCUS_GENERAL_VECTOR_STRENGTH = 3;
export const WORLD_FOCUS_HIGH_RISK_VECTOR_STRENGTH = 4;

export const WORLD_FOCUS_GENERAL_EXPECTED_INTERACTIONS = 4455;
export const WORLD_FOCUS_HIGH_RISK_EXPECTED_INTERACTIONS = 2835;

export const WORLD_FOCUS_GENERAL_VECTOR_SHA256 =
  'ca2e8b4aa19285eecd61ac072c0bc9a4f938e7863eea8393d2f2da26827610a0';
export const WORLD_FOCUS_HIGH_RISK_VECTOR_SHA256 =
  'd6efbcd0306ee7d37fac0b4cbc59c7af356c8ac8cbf9ee0d08ed8efbc8f5d835';

export const WORLD_FOCUS_GENERAL_3_WAY_VECTORS = Object.freeze([
  '00000121012',
  '02121012100',
  '22212220201',
  '11110102121',
  '11001210210',
  '20222001022',
  '00120210222',
  '22210111110',
  '20001022121',
  '11102011001',
  '01211202012',
  '21022102200',
  '12221120021',
  '10112020112',
  '02010001201',
  '01200020100',
  '20101100002',
  '12012212020',
  '22120222011',
  '10021201100',
  '12200002222',
  '01102121220',
  '00222211111',
  '21000211122',
  '20211112201',
  '21020000011',
  '02022100122',
  '11121221212',
  '00112002210',
  '10220122200',
  '11202112112',
  '21111110020',
  '22011221102',
  '02202200010',
  '11211021221',
  '10110221000',
  '22101001111',
  '01021010002',
  '00200212021',
  '10012100211',
  '22122112212',
  '12002022002',
  '20020011220',
  '01112210101',
  '02201111201',
  '00021122110',
  '02110010022',
  '20202220120',
  '10101202221',
  '21221022120',
  '10220010010',
  '01010122202',
  '12222101000',
  '02022222101',
  '20200200211',
  '20210002102',
  '12000110101',
  '01221120122',
  '22100002220',
  '20112121021',
  '12120000211',
  '00102200202',
  '21002001102',
  '12210221020',
  '21201221010',
  '02020220112',
  '01222102011',
] as const);

export const WORLD_FOCUS_HIGH_RISK_4_WAY_VECTORS = Object.freeze([
  '0111222',
  '2000211',
  '2220110',
  '0102020',
  '1201220',
  '1020020',
  '2011002',
  '1210101',
  '2022122',
  '0212012',
  '1122001',
  '2212221',
  '0012100',
  '0221121',
  '1102212',
  '1111110',
  '0100102',
  '2110200',
  '0021210',
  '2200022',
  '0120011',
  '1220202',
  '0202201',
  '2101121',
  '1201011',
  '1001102',
  '2002010',
  '1022111',
  '0221000',
  '0010021',
  '2121012',
  '1011201',
  '0210210',
  '2202100',
  '2010112',
  '1100221',
  '2122220',
  '1212122',
  '0002222',
  '2211020',
  '0112111',
  '0201112',
  '1110022',
  '2221201',
  '0000120',
  '0022002',
  '1100000',
  '2020101',
  '1222010',
  '0001001',
  '1012220',
  '2112001',
  '0220222',
  '2101210',
  '1121100',
  '1000012',
  '2222212',
  '1021222',
  '2211111',
  '2021021',
  '1120112',
  '1002021',
  '2112102',
  '0010202',
  '2110120',
  '0122200',
  '1202002',
  '1211212',
  '2001200',
  '0011010',
  '0101211',
  '2200001',
  '1200110',
  '0222120',
  '2101202',
  '1011121',
  '0211102',
  '2110010',
  '2012211',
  '0111001',
  '1212000',
  '1122121',
  '0002111',
  '1220211',
  '1101022',
  '0021112',
  '0122022',
  '2020000',
  '0200121',
  '2020222',
  '1112201',
  '1010210',
  '0101120',
  '1102101',
  '0022221',
  '2222011',
  '0200000',
  '2221102',
  '0100212',
  '2102112',
  '1121211',
  '0212021',
  '0112210',
  '2001120',
  '1002200',
  '0120101',
  '1011011',
  '1221022',
  '2200220',
  '0110221',
  '2120121',
  '2012022',
  '2210002',
  '0020110',
  '2100122',
  '1102120',
  '1222200',
  '2102021',
  '0121020',
  '1021000',
  '2122202',
  '1012212',
  '0220012',
  '1221110',
  '2111222',
  '1120210',
  '1000201',
  '0210122',
  '2202111',
  '0211200',
  '2110211',
  '1122012',
  '0001012',
  '1210021',
  '2021010',
  '2201000',
  '1111002',
  '1020120',
  '2002201',
  '2221122',
  '0110220',
  '2012110',
  '0200210',
  '0112112',
  '1221101',
  '1202221',
  '0021221',
  '0222011',
  '1022100',
  '0210100',
  '0112220',
  '1020202',
  '0201212',
  '0101102',
  '2002122',
  '1210111',
  '1101011',
] as const);

function assertVector(
  vector: string,
  expectedLength: number,
  label: string,
): string {
  if (vector.length !== expectedLength || !/^[012]+$/.test(vector)) {
    throw new Error(
      `${label} must contain exactly ${expectedLength} ternary digits`,
    );
  }
  return vector;
}

function chooseIndices(
  count: number,
  strength: number,
): readonly (readonly number[])[] {
  const result: number[][] = [];

  const visit = (start: number, selected: number[]) => {
    if (selected.length === strength) {
      result.push(selected.slice());
      return;
    }

    const remaining = strength - selected.length;
    for (let index = start; index <= count - remaining; index += 1) {
      selected.push(index);
      visit(index + 1, selected);
      selected.pop();
    }
  };

  visit(0, []);
  return Object.freeze(result.map((indices) => Object.freeze(indices)));
}

export function countWorldFocusCoveredInteractions(
  vectors: readonly string[],
  axisCount: number,
  strength: number,
): number {
  if (!Number.isInteger(axisCount) || axisCount <= 0) {
    throw new Error('World Focus combinatorial axis count must be positive');
  }
  if (
    !Number.isInteger(strength) ||
    strength <= 0 ||
    strength > axisCount
  ) {
    throw new Error('World Focus combinatorial strength is invalid');
  }

  const combinations = chooseIndices(axisCount, strength);
  const covered = new Set<string>();

  vectors.forEach((rawVector, rowIndex) => {
    const vector = assertVector(
      rawVector,
      axisCount,
      `World Focus combinatorial vector[${rowIndex}]`,
    );

    for (const indices of combinations) {
      const values = indices.map((index) => vector[index]).join('');
      covered.add(`${indices.join(',')}=${values}`);
    }
  });

  return covered.size;
}

export function serializeWorldFocusVectors(
  vectors: readonly string[],
  expectedLength: number,
): string {
  return vectors
    .map((vector, index) =>
      assertVector(
        vector,
        expectedLength,
        `World Focus combinatorial vector[${index}]`,
      ),
    )
    .join('\n');
}
