module Jekyll
  module DiscountFilters
    def discount_amount(value)
      return 0 unless value

      # Extract the first numeric value from the discount string
      match = value.to_s.scan(/[\d\.]+/).first
      match ? match.to_f : 0
    end

    def discounts_with_amount(coupons)
      return [] unless coupons.respond_to?(:select)

      coupons.select do |coupon|
        discount = coupon['discount_value'].to_s
        discount.match?(/[\%\$]/)
      end
    end

    def sort_by_savings(coupons)
      return [] unless coupons.respond_to?(:sort_by)

      coupons.sort_by { |coupon| -discount_amount(coupon['discount_value']) }
    end

    def strip_coupon_code(content, code)
      return content unless content && code

      stripped = content.dup
      patterns = [
        %r{<strong>\s*#{Regexp.escape(code)}\s*</strong>}i,
        %r{<b>\s*#{Regexp.escape(code)}\s*</b>}i,
        /#{Regexp.escape(code)}/i
      ]

      patterns.each do |pattern|
        stripped.gsub!(pattern, '')
      end

      stripped
    end
  end
end

Liquid::Template.register_filter(Jekyll::DiscountFilters)
