
""" Mã sinh viên: 202419115
    Họ tên: Đoàn Anh Tuấn """


from __future__ import annotations

import math
from typing import List, Optional, Tuple


# Hàm kiểm tra dữ liệu dùng chung (để giữ các bất biến)
def _require_text(value, name: str) -> str:
    """Chuỗi bắt buộc, không rỗng."""
    if not isinstance(value, str):
        raise TypeError(f"{name} phải là chuỗi (str)")
    if not value.strip():
        raise ValueError(f"{name} không được rỗng")
    return value.strip()


def _require_number(value, name: str) -> float:
    """Số thực hữu hạn."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} phải là số")
    if not math.isfinite(value):
        raise ValueError(f"{name} phải là số hữu hạn")
    return float(value)


def _require_non_negative(value, name: str) -> float:
    number = _require_number(value, name)
    if number < 0:
        raise ValueError(f"{name} không được âm")
    return number



# Lớp Employee
class Employee:
    """Nhân sự thông thường"""

    DEFAULT_ID = "UNKNOWN"
    DEFAULT_NAME = "Unnamed employee"

    def __init__(self, *args):
        if len(args) == 0:
            id_, full_name, salary = self.DEFAULT_ID, self.DEFAULT_NAME, 0.0
        elif len(args) == 2:
            id_, full_name = args
            salary = 0.0
        elif len(args) == 3:
            id_, full_name, salary = args
        else:
            raise TypeError(
                "Employee() nhận 0, 2 hoặc 3 tham số: "
                "(), (id, fullName), (id, fullName, baseSalary)"
            )

        id_ = _require_text(id_, "Mã nhân sự")
        full_name = _require_text(full_name, "Họ tên")
        salary = _require_non_negative(salary, "Lương cơ bản")

        self._id: str = id_
        self._fullName: str = full_name
        self._baseSalary: float = salary

    # ---- Getter ----
    def getId(self) -> str:
        return self._id

    def getFullName(self) -> str:
        return self._fullName

    def getBaseSalary(self) -> float:
        return self._baseSalary

    @property
    def id(self) -> str:                    
        return self._id

    @property
    def fullName(self) -> str:
        return self._fullName

    @fullName.setter
    def fullName(self, value: str) -> None:
        self._fullName = _require_text(value, "Họ tên")

    @property
    def baseSalary(self) -> float:
        return self._baseSalary

    @baseSalary.setter
    def baseSalary(self, value: float) -> None:
        self._baseSalary = _require_non_negative(value, "Lương cơ bản")

    # ---- Nạp chồng increaseSalary ----
    def increaseSalary(self, value: float,
                       byPercentage: Optional[bool] = None) -> None:
        amount = _require_number(value, "Giá trị tăng lương")
        if amount <= 0:
            raise ValueError("Giá trị tăng lương phải dương")
        if byPercentage is not None and not isinstance(byPercentage, bool):
            raise TypeError("byPercentage phải là bool")

        if byPercentage:                       # True -> theo phần trăm
            self._baseSalary += self._baseSalary * amount / 100.0
        else:                                  # None hoặc False -> cố định
            self._baseSalary += amount

    # ---- Phương thức đa hình ----
    def calculateMonthlyCost(self) -> float:
        return self._baseSalary

    def displayInfo(self) -> None:
        print(
            f"[Employee] id={self._id}, fullName={self._fullName}, "
            f"baseSalary={self._baseSalary:,.2f}, "
            f"monthlyCost={self.calculateMonthlyCost():,.2f}"
        )

    # ---- Destructor quan sát vòng đời ----
    def __del__(self):
        if not hasattr(self, "_id"):
            return
        try:
            print(f"[Destructor] ~Employee: '{self._id}' - {self._fullName}")
        except Exception:
            pass


# Lớp SoftwareEngineer (kế thừa Employee)
class SoftwareEngineer(Employee):
    """Kỹ sư phần mềm: Employee + ngôn ngữ chính + phụ cấp kỹ thuật."""

    def __init__(self, id_, fullName, *rest):
        if len(rest) == 1:
            salary, language, allowance = 0.0, rest[0], 0.0
        elif len(rest) == 3:
            salary, language, allowance = rest
        else:
            raise TypeError(
                "SoftwareEngineer() nhận (id, fullName, primaryLanguage) hoặc "
                "(id, fullName, baseSalary, primaryLanguage, technicalAllowance)"
            )

        language = _require_text(language, "Ngôn ngữ lập trình chính")
        allowance = _require_non_negative(allowance, "Phụ cấp kỹ thuật")

        super().__init__(id_, fullName, salary)     

        self._primaryLanguage: str = language
        self._technicalAllowance: float = allowance

    def getPrimaryLanguage(self) -> str:
        return self._primaryLanguage

    def getTechnicalAllowance(self) -> float:
        return self._technicalAllowance

    @property
    def primaryLanguage(self) -> str:
        return self._primaryLanguage

    @primaryLanguage.setter
    def primaryLanguage(self, value: str) -> None:
        self._primaryLanguage = _require_text(value, "Ngôn ngữ lập trình chính")

    @property
    def technicalAllowance(self) -> float:
        return self._technicalAllowance

    @technicalAllowance.setter
    def technicalAllowance(self, value: float) -> None:
        self._technicalAllowance = _require_non_negative(value, "Phụ cấp kỹ thuật")

    # ---- Ghi đè caculateMonthlyCost và displayInfo ----
    def calculateMonthlyCost(self) -> float:
        return self._baseSalary + self._technicalAllowance

    def displayInfo(self) -> None:
        print(
            f"[SoftwareEngineer] id={self._id}, fullName={self._fullName}, "
            f"baseSalary={self._baseSalary:,.2f}, "
            f"primaryLanguage={self._primaryLanguage}, "
            f"technicalAllowance={self._technicalAllowance:,.2f}, "
            f"monthlyCost={self.calculateMonthlyCost():,.2f}"
        )

    def __del__(self):
        if hasattr(self, "_primaryLanguage"):
            try:
                print(f"[Destructor] ~SoftwareEngineer: '{self._id}' - "
                      f"{self._fullName}")
            except Exception:
                pass
        super().__del__()



# Lớp ProjectTeam
class ProjectTeam:
    def __init__(self, projectCode: str, projectName: str,
                 leader: Optional[Employee] = None):
        code = _require_text(projectCode, "Mã dự án")
        name = _require_text(projectName, "Tên dự án")
        if leader is not None:
            self._check_employee(leader)

        self._projectCode: str = code
        self._projectName: str = name
        self._leader: Optional[Employee] = None
        self._members: List[Employee] = []

        if leader is not None:
            self.addMember(leader, True)

    @property
    def projectCode(self) -> str:
        return self._projectCode

    @property
    def projectName(self) -> str:
        return self._projectName

    @property
    def leader(self) -> Optional[Employee]:
        return self._leader

    @property
    def members(self) -> Tuple[Employee, ...]:
        return tuple(self._members)           
    
    @staticmethod
    def _check_employee(employee) -> None:
        if not isinstance(employee, Employee):
            raise TypeError("Đối số phải là đối tượng Employee (hoặc lớp con)")

    def _find(self, employeeId: str) -> Optional[Employee]:
        for m in self._members:
            if m.getId() == employeeId:
                return m
        return None

    # ---- Nạp chồng addMember ----
    def addMember(self, employee: Employee, makeLeader: bool = False) -> bool:
        self._check_employee(employee)
        if not isinstance(makeLeader, bool):
            raise TypeError("makeLeader phải là bool")

        existing = self._find(employee.getId())
        if existing is not None and existing is not employee:
            raise ValueError(
                f"Đã có một nhân sự khác mang mã '{employee.getId()}' trong nhóm"
            )

        added = existing is None
        if added:
            self._members.append(employee)
        if makeLeader:
            self._leader = employee           
        return added

    def removeMember(self, employeeId: str) -> bool:
        if not isinstance(employeeId, str):
            raise TypeError("employeeId phải là chuỗi")
        if self._leader is not None and self._leader.getId() == employeeId:
            raise ValueError(
                "Không được xóa trưởng nhóm khi chưa chọn trưởng nhóm thay thế "
                "(hãy gọi changeLeader() trước)"
            )
        for i, m in enumerate(self._members):
            if m.getId() == employeeId:
                del self._members[i]
                return True
        return False

    def changeLeader(self, employee: Employee) -> None:
        # Nếu chưa là thành viên thì addMember sẽ thêm vào; trưởng nhóm cũ
        # vẫn ở lại trong danh sách.
        self.addMember(employee, True)

    def contains(self, employeeId: str) -> bool:
        return self._find(employeeId) is not None

    def calculateTotalMonthlyCost(self) -> float:
        return sum(m.calculateMonthlyCost() for m in self._members)

    def displayTeam(self) -> None:
        leader_name = self._leader.getFullName() if self._leader else "(chưa có)"
        print(f"--- Nhóm {self._projectCode} - {self._projectName} "
              f"(Trưởng nhóm: {leader_name}) ---")
        if not self._members:
            print("  (chưa có thành viên)")
        for m in self._members:
            m.displayInfo()                    
        print(f"Tổng chi phí hằng tháng: {self.calculateTotalMonthlyCost():,.2f}")
        print("-" * 60)

    def __del__(self):
        if not hasattr(self, "_members"):
            return
        try:
            print(f"[Destructor] ~ProjectTeam: '{self._projectCode}' bị hủy "
                  f"(các Employee thành viên KHÔNG bị hủy theo)")
        except Exception:
            pass
        self._members.clear()
        self._leader = None



# KIỂM THỬ
_passed = 0
_failed = 0


def header(text: str) -> None:
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def check(label: str, condition: bool, extra: str = "") -> None:
    global _passed, _failed
    if condition:
        _passed += 1
        print(f"  [PASS] {label} {extra}")
    else:
        _failed += 1
        print(f"  [FAIL] {label} {extra}")


def expect_raises(label: str, exc_type, func, *args) -> None:
    try:
        func(*args)
    except exc_type as ex:
        check(label, True, f"-> {type(ex).__name__}: {ex}")
    except Exception as ex:                     
        check(label, False, f"-> ném {type(ex).__name__} thay vì {exc_type.__name__}")
    else:
        check(label, False, "-> không ném ngoại lệ")


def run_scenario():
    """Kịch bản 15 trường hợp kiểm thử."""
    header("1. Tạo hai Employee bằng hai constructor khác nhau")
    e1 = Employee("NV001", "Nguyen Van A")                
    e2 = Employee("NV002", "Tran Thi B", 8_000_000)       
    e1.displayInfo()
    e2.displayInfo()

    header("2. Tạo hai SoftwareEngineer bằng hai constructor khác nhau")
    se1 = SoftwareEngineer("KS001", "Le Van C", "Python")
    se2 = SoftwareEngineer("KS002", "Pham Thi D", 12_000_000, "C++", 1_500_000)
    se1.displayInfo()
    se2.displayInfo()

    header("3. Tăng lương một nhân sự bằng số tiền cố định (e2 + 500.000)")
    e2.increaseSalary(500_000)
    e2.displayInfo()

    header("4. Tăng lương một nhân sự khác theo phần trăm (se2 + 10%)")
    se2.increaseSalary(10, True)
    se2.displayInfo()

    header("5. Tạo nhóm dự án không có trưởng nhóm")
    team1 = ProjectTeam("PRJ01", "Website Ban Hang")
    team1.displayTeam()

    header("6. Thêm một nhân sự vào nhóm bằng addMember(employee)")
    print("addMember(e1) =", team1.addMember(e1))
    team1.displayTeam()

    header("7. Thêm một kỹ sư bằng addMember(employee, True) -> làm trưởng nhóm")
    print("addMember(se1, True) =", team1.addMember(se1, True))
    team1.displayTeam()

    header("8. Thử thêm lại một thành viên đã tồn tại (kỳ vọng False)")
    result = team1.addMember(e1)
    print("addMember(e1) lần 2 =", result)
    check("Không thêm trùng", result is False and len(team1.members) == 2)

    header("9. Hiển thị danh sách bằng lời gọi đa hình")
    team1.addMember(e2)
    team1.addMember(se2)
    team1.displayTeam()

    header("10. Tính tổng chi phí nhân sự hằng tháng")
    total = team1.calculateTotalMonthlyCost()
    print(f"Tổng chi phí nhóm {team1.projectCode}: {total:,.2f}")
    check("Tổng = 0 + 0 + 8.500.000 + 14.700.000", total == 23_200_000)

    header("11. Thử xóa trưởng nhóm hiện tại -> kỳ vọng bị từ chối")
    expect_raises("Xóa trưởng nhóm bị từ chối", ValueError,
                  team1.removeMember, se1.getId())
    check("Trưởng nhóm vẫn còn trong danh sách", team1.contains(se1.getId()))

    header("12. Đổi trưởng nhóm rồi xóa người từng là trưởng nhóm")
    team1.changeLeader(e2)
    removed = team1.removeMember(se1.getId())
    print("Xóa se1 sau khi đổi trưởng nhóm =", removed)
    check("se1 đã bị xóa khỏi nhóm 1", removed and not team1.contains(se1.getId()))
    team1.displayTeam()

    header("13. Tạo nhóm thứ hai, thêm nhân sự đã có ở nhóm 1 (kết tập nhiều nhóm)")
    header("14. Hủy nhóm thứ hai bằng cách kết thúc một khối lệnh cục bộ")

    def local_block():
        team2 = ProjectTeam("PRJ02", "Ung Dung Mobile", e2)   # e2 đã ở team1
        team2.addMember(se2)                                   # se2 đã ở team1
        team2.displayTeam()
        check("e2 thuộc cả team1 và team2",
              team1.contains(e2.getId()) and team2.contains(e2.getId()))
        print(">> Kết thúc khối lệnh cục bộ: team2 sắp bị hủy...")

    local_block()
    print(">> Đã thoát khối lệnh: dòng [Destructor] ~ProjectTeam ở trên là của team2.")

    header("15. Chứng minh nhân sự của nhóm 2 vẫn tồn tại sau khi nhóm 2 bị hủy")
    e2.displayInfo()
    se2.displayInfo()
    check("e2 và se2 vẫn dùng được, không có Destructor Employee nào bị in "
          "giữa bước 14 và 15", True)
    check("e2 vẫn thuộc team1", team1.contains(e2.getId()))
    check("se2 vẫn thuộc team1", team1.contains(se2.getId()))
    
def run_edge_cases():
    """Các trường hợp biên."""
    header(" CÁC TRƯỜNG HỢP BIÊN")

    print("\n-- Employee: dữ liệu không hợp lệ --")
    expect_raises("id rỗng", ValueError, Employee, "", "Ten")
    expect_raises("id chỉ toàn khoảng trắng", ValueError, Employee, "   ", "Ten")
    expect_raises("họ tên rỗng", ValueError, Employee, "X1", "")
    expect_raises("lương âm", ValueError, Employee, "X1", "Ten", -1)
    expect_raises("lương NaN", ValueError, Employee, "X1", "Ten", float("nan"))
    expect_raises("lương là chuỗi", TypeError, Employee, "X1", "Ten", "abc")
    expect_raises("id không phải chuỗi", TypeError, Employee, 123, "Ten")
    expect_raises("sai số lượng tham số (1)", TypeError, Employee, "X1")
    expect_raises("sai số lượng tham số (4)", TypeError, Employee, "a", "b", 1, 2)

    d = Employee()
    check("Constructor mặc định", d.getId() == "UNKNOWN"
          and d.getFullName() == "Unnamed employee" and d.getBaseSalary() == 0)
    z = Employee("Z0", "Luong Bang Khong", 0)
    check("Lương = 0 hợp lệ (biên dưới)", z.getBaseSalary() == 0)

    print("\n-- Employee: bảo vệ bất biến khi gán trực tiếp --")
    expect_raises("gán baseSalary âm", ValueError, setattr, z, "baseSalary", -5)
    expect_raises("gán fullName rỗng", ValueError, setattr, z, "fullName", "")
    expect_raises("đổi id (chỉ đọc)", AttributeError, setattr, z, "id", "Z9")

    print("\n-- increaseSalary --")
    expect_raises("tăng 0", ValueError, z.increaseSalary, 0)
    expect_raises("tăng số âm", ValueError, z.increaseSalary, -100)
    expect_raises("tăng % số âm", ValueError, z.increaseSalary, -10, True)
    expect_raises("tăng % bằng 0", ValueError, z.increaseSalary, 0, True)
    expect_raises("byPercentage không phải bool", TypeError, z.increaseSalary, 5, 1)
    z.increaseSalary(10, True)
    check("Tăng % trên lương 0 vẫn là 0", z.getBaseSalary() == 0)
    y = Employee("Y1", "Tang 100 Phan Tram", 1000)
    y.increaseSalary(100, True)
    check("Tăng 100% -> gấp đôi", y.getBaseSalary() == 2000)
    y.increaseSalary(50, False)
    check("byPercentage=False -> tăng cố định 50", y.getBaseSalary() == 2050)
    y.increaseSalary(1_000_000, True)
    check("Tăng % rất lớn vẫn hợp lệ", y.getBaseSalary() > 2050)

    print("\n-- SoftwareEngineer: dữ liệu không hợp lệ --")
    expect_raises("ngôn ngữ rỗng", ValueError, SoftwareEngineer, "K1", "Ten", "")
    expect_raises("phụ cấp âm", ValueError, SoftwareEngineer,
                  "K1", "Ten", 1000, "Java", -1)
    expect_raises("lương âm", ValueError, SoftwareEngineer,
                  "K1", "Ten", -1, "Java", 0)
    expect_raises("id rỗng (không được in destructor cho đối tượng lỗi)",
                  ValueError, SoftwareEngineer, "", "Ten", "Java")
    expect_raises("sai số lượng tham số", TypeError,
                  SoftwareEngineer, "K1", "Ten", 1000, "Java")
    ok = SoftwareEngineer("K0", "Phu Cap Bang 0", 1000, "Go", 0)
    check("Phụ cấp = 0 hợp lệ; chi phí = lương", ok.calculateMonthlyCost() == 1000)
    check("Đa hình: SoftwareEngineer là một Employee", isinstance(ok, Employee))

    print("\n-- ProjectTeam: dữ liệu không hợp lệ --")
    expect_raises("mã dự án rỗng", ValueError, ProjectTeam, "", "Ten")
    expect_raises("tên dự án rỗng", ValueError, ProjectTeam, "P", "  ")
    expect_raises("leader không phải Employee", TypeError, ProjectTeam, "P", "N", "abc")

    print("\n-- ProjectTeam: nhóm rỗng và trưởng nhóm qua constructor --")
    empty = ProjectTeam("E00", "Nhom Rong")
    check("Nhóm rỗng: tổng chi phí = 0", empty.calculateTotalMonthlyCost() == 0)
    check("Nhóm rỗng: removeMember ID không tồn tại -> False",
          empty.removeMember("NOPE") is False)
    empty.displayTeam()

    boss = Employee("B1", "Truong Nhom", 5000)
    member = Employee("M1", "Thanh Vien", 3000)
    t = ProjectTeam("T01", "Nhom Co Truong Nhom", boss)
    check("Constructor 2 tự đưa leader vào members",
          t.contains("B1") and t.leader is boss and len(t.members) == 1)
    check("Thêm trùng chính trưởng nhóm -> False, không nhân đôi",
          t.addMember(boss) is False and len(t.members) == 1)

    print("\n-- ProjectTeam: addMember / changeLeader / removeMember --")
    expect_raises("addMember(None)", TypeError, t.addMember, None)
    expect_raises("makeLeader không phải bool", TypeError, t.addMember, member, "yes")
    clone = Employee("M1", "Nguoi Khac Cung Ma", 1)
    t.addMember(member)
    expect_raises("Đối tượng khác nhưng trùng mã bị từ chối", ValueError,
                  t.addMember, clone)
    expect_raises("changeLeader bằng đối tượng trùng mã", ValueError,
                  t.changeLeader, clone)
    check("Sau lỗi, trưởng nhóm vẫn là boss", t.leader is boss)

    check("addMember(đã có, True) -> False nhưng đổi trưởng nhóm",
          t.addMember(member, True) is False and t.leader is member)
    check("Trưởng nhóm cũ vẫn là thành viên", t.contains("B1"))

    newcomer = Employee("N1", "Nguoi Moi", 2000)
    t.changeLeader(newcomer)
    check("changeLeader với người chưa là thành viên -> được thêm vào",
          t.contains("N1") and t.leader is newcomer)
    expect_raises("Xóa trưởng nhóm mới bị từ chối", ValueError, t.removeMember, "N1")
    check("removeMember ID không tồn tại -> False", t.removeMember("NOPE") is False)
    check("removeMember thành viên thường -> True", t.removeMember("B1") is True)
    expect_raises("removeMember(ID không phải chuỗi)", TypeError, t.removeMember, 5)

    print("\n-- Bảo vệ danh sách thành viên --")
    expect_raises("members là tuple, không append được", AttributeError,
                  lambda: t.members.append(boss))
    expect_raises("gán trực tiếp leader bị chặn", AttributeError,
                  setattr, t, "leader", boss)

    print("\n-- Một nhân sự thuộc nhiều nhóm --")
    t_other = ProjectTeam("T02", "Nhom Khac", newcomer)
    check("newcomer thuộc cả hai nhóm", t.contains("N1") and t_other.contains("N1"))
    del t_other
    check("Hủy nhóm khác, newcomer vẫn còn trong nhóm T01", t.contains("N1"))
    print(f"  newcomer vẫn dùng được: {newcomer.getFullName()}")


def main():
    header(" KIỂM THỬ 15 KỊCH BẢN ")
    run_scenario()
    run_edge_cases()
    header("TỔNG KẾT")
    print(f"PASS: {_passed}   FAIL: {_failed}")


if __name__ == "__main__":
    main()
